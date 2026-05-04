from src.core.exchange import TradingPlatform
from src.core.order import Order, OrderType
from src.core.participant import Trader
from src.exceptions.custom_exceptions import ExchangeBaseException
from src.interface.exchange_manager import ExchangeManager


class ExchangeCLI:
    """Класс для работы с интерфейсом командной строки."""

    def __init__(self, manager: ExchangeManager, platform: TradingPlatform, trader: Trader):
        self.manager = manager
        self.platform = platform
        self.trader = trader

    def display_menu(self) -> None:
        print("\n--- Валютно-фондовая биржа ---")
        print("1. Анализ рынка (Список активов)")
        print("2. Мой портфель")
        print("3. Купить актив")
        print("4. Продать актив")
        print("5. Обновление цен")
        print("6. Выход")

    def run(self) -> None:
        """Главный цикл работы программы."""
        print(f"Добро пожаловать, {self.trader.name}! Базовая валюта: {self.manager.base_currency}")
        
        while True:
            self.display_menu()
            choice = input("Выберите действие (1-6): ").strip()

            try:
                if choice == '1':
                    print("\n" + self.manager.analyze_market(self.platform))
                elif choice == '2':
                    print("\n" + self.manager.get_portfolio_summary(self.trader))
                elif choice == '3':
                    self._handle_trade(OrderType.BUY)
                elif choice == '4':
                    self._handle_trade(OrderType.SELL)
                elif choice == '5':
                    print("\n" + self.manager.simulate_market_tick())
                    input("\nНажмите Enter для возврата в меню...")
                elif choice == '6':
                    print("Завершение работы. До свидания!")
                    break
                else:
                    print("Неверный ввод. Пожалуйста, введите число от 1 до 6.")
            
            # Перехват наших пользовательских исключений и ошибок ввода
            except ExchangeBaseException as e:
                print(f"\n[Ошибка Биржи]: {e}")
            except ValueError as e:
                print(f"\n[Ошибка Ввода]: {e}")
            except Exception as e:
                print(f"\n[Непредвиденная ошибка]: {e}")

    def _handle_trade(self, order_type: OrderType) -> None:
        """Вспомогательный метод для сбора данных о сделке от пользователя."""
        ticker = input("Введите тикер актива (например, USD, AAPL): ").strip().upper()
        amount_str = input("Введите количество: ").strip()
        price_str = input("Введите цену за единицу: ").strip()

        # Преобразуем ввод и ловим ValueError, если ввели не числа
        amount = float(amount_str)
        price = float(price_str)

        # Формируем заявку (операция оформления заявок)
        order = Order(
            trader=self.trader,
            order_type=order_type,
            ticker=ticker,
            amount=amount,
            price=price
        )

        # Передаем заявку менеджеру на исполнение
        result_message = self.manager.process_order(order)
        print("\n[Результат]: " + result_message)