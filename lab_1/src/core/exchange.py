import random
from typing import Dict, List

from src.core.asset import Asset
from src.core.participant import Broker
from src.exceptions.custom_exceptions import AssetNotFoundError

# Отвечает за регистрацию доступных торговых инструментов и брокеров.
class Exchange:

    def __init__(self, name: str):
        self.name = name
        self._assets: Dict[str, Asset] = {}
        self._brokers: List[Broker] = []

    def add_asset(self, asset: Asset) -> None:
        self._assets[asset.ticker] = asset

    def get_asset(self, ticker: str) -> Asset:
        if ticker not in self._assets:
            raise AssetNotFoundError(f"Актив с тикером '{ticker}' не торгуется на бирже {self.name}.")
        return self._assets[ticker]

    # Допускает брокера к торгам на данной бирже.
    def register_broker(self, broker: Broker) -> None:
        if broker not in self._brokers:
            self._brokers.append(broker)

    def get_brokers(self) -> List[Broker]:
        return self._brokers.copy()
    # Возвращает словарь всех доступных активов.
    def get_all_assets(self) -> Dict[str, Asset]:
        return self._assets.copy()

    def simulate_market_tick(self) -> Dict[str, tuple[float, float]]:
        
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

    def __init__(self, name: str, exchange: Exchange):
        self.name = name
        self.exchange = exchange
    # Операция анализа рынка: собирает информацию по всем активам биржи.
    def get_market_data(self) -> str:
        assets = self.exchange.get_all_assets()
        if not assets:
            return "Рынок пуст. Активы не добавлены в листинг."
        
        info_lines = [f"=== Сводка рынка (Платформа: {self.name} | Биржа: {self.exchange.name}) ==="]
        for asset in assets.values():
            info_lines.append(asset.get_asset_info())
            
        return "\n".join(info_lines)