import unittest

# from exchange_project import Exchange, Stock, Broker, Trader, ExchangeManager, Order, OrderType, InsufficientFundsError, InvalidTransactionError

from src.core.exchange import Exchange, TradingPlatform
from src.core.asset import Stock
from src.core.participant import Broker, Trader
from src.core.order import Order, OrderType
from src.interface.exchange_manager import ExchangeManager
from src.exceptions.custom_exceptions import InsufficientFundsError, InvalidTransactionError


class TestExchangeManager(unittest.TestCase):
    """Набор тестов для проверки бизнес-логики менеджера биржи."""

    def setUp(self):
        """Этот метод автоматически запускается ПЕРЕД каждым тестом.
        Здесь мы создаем 'чистую' тестовую среду."""
        
        self.exchange = Exchange("Тестовая Биржа")
        self.manager = ExchangeManager(self.exchange, base_currency="USD")
        
        # Создаем тестовый актив (акция по цене 100 USD)
        self.apple_stock = Stock("AAPL", "Apple Inc.", initial_price=100.0, total_shares=1000)
        self.exchange.add_asset(self.apple_stock)
        
        # Создаем брокера с комиссией 1% (0.01)
        self.broker = Broker("Тестовый Брокер", commission_rate=0.01)
        self.exchange.register_broker(self.broker)
        
        # Создаем трейдера и выдаем ему 1000 USD
        self.trader = Trader("Тестовый Трейдер")
        self.broker.register_trader(self.trader)
        self.trader.portfolio.deposit("USD", 1000.0)

    def test_successful_buy_order(self):
        """Тест: Успешная покупка актива с правильным списанием комиссии."""
        # Трейдер хочет купить 2 акции по 100 USD.
        # Общая стоимость = 200. Комиссия (1%) = 2. Итого к списанию = 202 USD.
        order = Order(self.trader, OrderType.BUY, "AAPL", amount=2.0, price=100.0)
        
        # Выполняем заявку
        self.manager.process_order(order)
        
        # Проверяем, что балансы изменились правильно (assert - утверждение)
        self.assertEqual(self.trader.portfolio.get_balance("USD"), 798.0) # 1000 - 202
        self.assertEqual(self.trader.portfolio.get_balance("AAPL"), 2.0)
        self.assertEqual(self.broker.portfolio.get_balance("USD"), 2.0)   # Брокер получил комиссию

    def test_insufficient_funds_buy(self):
        """Тест: Ошибка при попытке купить активы, если не хватает денег."""
        # Трейдер пытается купить 20 акций по 100 USD (нужно 2000 + комиссия, а есть только 1000)
        order = Order(self.trader, OrderType.BUY, "AAPL", amount=20.0, price=100.0)
        
        # Ожидаем, что выбросится наше кастомное исключение InsufficientFundsError
        with self.assertRaises(InsufficientFundsError):
            self.manager.process_order(order)
            
        # Проверяем, что деньги НЕ списались (транзакция отменилась)
        self.assertEqual(self.trader.portfolio.get_balance("USD"), 1000.0)
        self.assertEqual(self.trader.portfolio.get_balance("AAPL"), 0.0)

    def test_price_mismatch(self):
        """Тест: Защита от покупки по неактуальной рыночной цене."""
        # Рыночная цена AAPL - 100. Трейдер хитрит и ставит цену 50.
        order = Order(self.trader, OrderType.BUY, "AAPL", amount=2.0, price=50.0)
        
        with self.assertRaises(InvalidTransactionError):
            self.manager.process_order(order)

    def test_successful_sell_order(self):
        """Тест: Успешная продажа актива."""
        # Сначала "подарим" трейдеру 5 акций для продажи
        self.trader.portfolio.deposit("AAPL", 5.0)
        
        # Трейдер продает 3 акции по 100 USD. 
        # Выручка = 300. Комиссия (1%) = 3. Чистыми получит 297 USD.
        order = Order(self.trader, OrderType.SELL, "AAPL", amount=3.0, price=100.0)
        self.manager.process_order(order)
        
        # Проверяем балансы
        self.assertEqual(self.trader.portfolio.get_balance("AAPL"), 2.0) # 5 - 3
        self.assertEqual(self.trader.portfolio.get_balance("USD"), 1297.0) # 1000 + 297
        self.assertEqual(self.broker.portfolio.get_balance("USD"), 3.0)

    def test_negative_amount_validation(self):
        """Тест: Дескриптор ловит попытку создать ордер с отрицательным количеством."""
        with self.assertRaises(ValueError):
            # Передаем -5 в amount (должна сработать защита дескриптора ValidatedNumber)
            Order(self.trader, OrderType.BUY, "AAPL", amount=-5.0, price=100.0)


if __name__ == "__main__":
    unittest.main()