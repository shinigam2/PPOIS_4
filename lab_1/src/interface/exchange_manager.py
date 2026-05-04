from src.core.exchange import Exchange, TradingPlatform
from src.core.order import Order, OrderType
from src.core.participant import Trader
from src.exceptions.custom_exceptions import InvalidTransactionError


class ExchangeManager:
    """
    Класс бизнес-логики.
    Отвечает за проведение торговых операций (расчеты) и управление портфелями.
    """

    def __init__(self, exchange: Exchange, base_currency: str = "USD"):
        self.exchange = exchange
        self.base_currency = base_currency

    def process_order(self, order: Order) -> str:
        """
        Операция оформления и исполнения торговой заявки.
        Маршрутизирует логику в зависимости от типа ордера (Покупка/Продажа).
        """
        # Проверяем, существует ли актив на бирже (если нет, биржа выбросит AssetNotFoundError)
        asset = self.exchange.get_asset(order.ticker)
        
        # Защита от попытки купить/продать по цене, отличающейся от рыночной 
        if order.price != asset.price:
            raise InvalidTransactionError(
                f"Цена в заявке ({order.price}) не совпадает с рыночной ({asset.price})."
            )

        # Вызываем нужный метод и ОБЯЗАТЕЛЬНО возвращаем его результат (return)
        if order.order_type == OrderType.BUY:
            return self._execute_buy(order)
        elif order.order_type == OrderType.SELL:
            return self._execute_sell(order)
        else:
            raise ValueError("Неизвестный тип заявки.")

    def _execute_buy(self, order: Order) -> str:
        """Внутренний метод для расчетов при покупке."""
        broker = order.trader.get_broker()
        total_cost = order.get_total_value()
        commission = total_cost * broker.commission_rate
        total_deduction = total_cost + commission

        # Проверяем и списываем базовую валюту (например, USD)
        order.trader.portfolio.withdraw(self.base_currency, total_deduction)
        
        # Начисляем комиссию брокеру
        broker.portfolio.deposit(self.base_currency, commission)
        
        # Начисляем купленный актив трейдеру
        order.trader.portfolio.deposit(order.ticker, order.amount)

        return (f"Успешно: {order.trader.name} купил {order.amount} '{order.ticker}'. "
                f"Списано: {total_deduction} {self.base_currency} (вкл. комиссию {commission}).")

    def _execute_sell(self, order: Order) -> str:
        """Внутренний метод для расчетов при продаже."""
        broker = order.trader.get_broker()
        
        # Сначала пробуем списать продаваемый актив (если его нет, выпадет ошибка)
        order.trader.portfolio.withdraw(order.ticker, order.amount)
        
        total_revenue = order.get_total_value()
        commission = total_revenue * broker.commission_rate
        net_revenue = total_revenue - commission

        # Начисляем комиссию брокеру
        broker.portfolio.deposit(self.base_currency, commission)
        
        # Начисляем выручку трейдеру
        order.trader.portfolio.deposit(self.base_currency, net_revenue)

        # Обязательно возвращаем строку с результатом
        return (f"Успешно: {order.trader.name} продал {order.amount} '{order.ticker}'. "
                f"Получено: {net_revenue} {self.base_currency} (удержана комиссия {commission}).")

    def get_portfolio_summary(self, trader: Trader) -> str:
        """Операция управления портфелем: получение сводки балансов."""
        balances = trader.portfolio.get_all_balances()
        if not balances:
            return f"Портфель трейдера {trader.name} пуст."
        
        lines = [f"=== Портфель ({trader.name}) ==="]
        for ticker, amount in balances.items():
            lines.append(f" - {ticker}: {amount}")
        return "\n".join(lines)

    def analyze_market(self, platform: TradingPlatform) -> str:
        """Делегирование операции анализа рынка торговой платформе."""
        return platform.get_market_data()
    
    def simulate_market_tick(self) -> str:
        """
        Делегирует симуляцию рыночного тика в доменный слой.
        Возвращает отформатированную строку для вывода в CLI.
        """
        changes = self.exchange.simulate_market_tick()
        
        if not changes:
            return "Нет активов для обновления."
        
        lines = ["Обновление цен завершено:", "-" * 40]
        for ticker, (old, new) in changes.items():
            delta = ((new - old) / old) * 100 if old != 0 else 0
            arrow = "^" if delta >= 0 else "v"
            lines.append(f"{arrow} {ticker}: {old:.2f} → {new:.2f} ({delta:+.1f}%)")
        lines.append("-" * 40)
        
        return "\n".join(lines)