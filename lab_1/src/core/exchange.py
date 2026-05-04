import random
from typing import Dict, List

from src.core.asset import Asset
from src.core.participant import Broker
from src.exceptions.custom_exceptions import AssetNotFoundError


class Exchange:
    """
    Центральный класс Биржи. 
    Отвечает за регистрацию доступных торговых инструментов и брокеров.
    """
    def __init__(self, name: str):
        self.name = name
        self._assets: Dict[str, Asset] = {}
        self._brokers: List[Broker] = []

    def add_asset(self, asset: Asset) -> None:
        """Добавляет новый актив (валюту, акцию или индекс) в листинг биржи."""
        self._assets[asset.ticker] = asset

    def get_asset(self, ticker: str) -> Asset:
        """Возвращает актив по тикеру. Вызывает исключение, если он не найден."""
        if ticker not in self._assets:
            raise AssetNotFoundError(f"Актив с тикером '{ticker}' не торгуется на бирже {self.name}.")
        return self._assets[ticker]

    def register_broker(self, broker: Broker) -> None:
        """Допускает брокера к торгам на данной бирже."""
        if broker not in self._brokers:
            self._brokers.append(broker)

    def get_brokers(self) -> List[Broker]:
        return self._brokers.copy()

    def get_all_assets(self) -> Dict[str, Asset]:
        """Возвращает словарь всех доступных активов."""
        return self._assets.copy()

    def simulate_market_tick(self) -> Dict[str, tuple[float, float]]:
        """
        Симулирует рыночный тик: изменяет цены всех активов в пределах ±5%
        от их начальной стоимости.
        Возвращает: {ticker: (old_price, new_price)}
        """
        changes: Dict[str, tuple[float, float]] = {}

        for asset in self._assets.values():
            old_price = asset.price
            
            volatility = random.uniform(-0.05, 0.05)
            new_price = asset.initial_price * (1 + volatility)
            new_price = max(new_price, 0.01)
            
            asset.update_price(new_price)
            changes[asset.ticker] = (old_price, new_price)

        return changes

class TradingPlatform:
    """
    Торговая платформа.
    Выступает как интерфейс для анализа рынка и взаимодействия с конкретной биржей.
    """
    def __init__(self, name: str, exchange: Exchange):
        self.name = name
        self.exchange = exchange

    def get_market_data(self) -> str:
        """Операция анализа рынка: собирает информацию по всем активам биржи."""
        assets = self.exchange.get_all_assets()
        if not assets:
            return "Рынок пуст. Активы не добавлены в листинг."
        
        info_lines = [f"=== Сводка рынка (Платформа: {self.name} | Биржа: {self.exchange.name}) ==="]
        for asset in assets.values():
            # Благодаря полиморфизму нам не важно, акция это, валюта или индекс.
            # Метод get_asset_info() отработает корректно для каждого.
            info_lines.append(asset.get_asset_info())
            
        return "\n".join(info_lines)