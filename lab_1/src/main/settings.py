from src.core.asset import Currency, Stock, MarketIndex
from src.core.exchange import Exchange, TradingPlatform
from src.core.participant import Broker, Trader
from src.interface.exchange_manager import ExchangeManager


def setup_exchange() -> tuple[ExchangeManager, TradingPlatform, Trader]:
    """Инициализация стартовых данных для симуляции."""
    
    # 1. Создаем биржу и платформу
    exchange = Exchange(name="Главная Биржа")
    platform = TradingPlatform(name="КвикТрейд Про", exchange=exchange)
    manager = ExchangeManager(exchange=exchange, base_currency="USD")

    # 2. Создаем активы
    usd = Currency(ticker="USD", name="Доллар", initial_price=1, country="США")
    eur = Currency(ticker="EUR", name="Евро", initial_price=1.08, country="ЕС")
    apple_stock = Stock(ticker="AAPL", company_name="Apple Inc.", initial_price=175.5, total_shares=1000)
    
    # Создаем индекс и добавляем в него активы
    tech_index = MarketIndex(ticker="TECH", name="Tech Index", initial_value=3250.0)
    tech_index.add_component(apple_stock)

    # Добавляем активы на биржу
    for asset in [usd, eur, apple_stock, tech_index]:
        exchange.add_asset(asset)

    # 3. Создаем участников
    broker = Broker(name="Брокер 'Надежный'", commission_rate=0.02) # Комиссия 2%
    exchange.register_broker(broker)

    trader = Trader(name="Михаил")
    broker.register_trader(trader)

    # Выдаем трейдеру стартовый баланс в базовой валюте
    trader.portfolio.deposit("USD", 10000.0)

    return manager, platform, trader