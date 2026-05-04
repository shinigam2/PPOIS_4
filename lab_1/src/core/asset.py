from abc import ABC, abstractmethod
from typing import List

from src.utils.descriptor import ValidatedNumber


class Asset(ABC):
    
    price = ValidatedNumber(min_value=0, allow_zero=False)

    def __init__(self, ticker: str, name: str, initial_price: float):
        self.ticker = ticker
        self.name = name
        self._initial_price = initial_price  # Запоминаем базовое знач
        self.price = initial_price

    @property
    def initial_price(self) -> float:
        return self._initial_price

    @abstractmethod
    def get_asset_info(self) -> str:
        pass

    def update_price(self, new_price: float) -> None:
        self.price = round(new_price, 2)

    def __str__(self) -> str:
        return f"{self.ticker} - {self.price}"

# Класс представляющий валюту
class Currency(Asset):

    def __init__(self, ticker: str, name: str, initial_price: float, country: str):
        super().__init__(ticker, name, initial_price)
        self.country = country

    def get_asset_info(self) -> str:
        return f"[Валюта] {self.name} ({self.country}). Тикер: {self.ticker}, Курс: {self.price}"

# Акции компании
class Stock(Asset):
    
    total_shares = ValidatedNumber(min_value=0, allow_zero=True)

    def __init__(self, ticker: str, company_name: str, initial_price: float, total_shares: int):
        super().__init__(ticker, company_name, initial_price)
        self.total_shares = total_shares

    def get_asset_info(self) -> str:
        return (f"[Акция] {self.name}. Тикер: {self.ticker}, "
                f"Цена: {self.price}, Выпущено акций: {self.total_shares}")

# Класс, представляющий рыночный индекс. Объединяет другие активы для анализа рынка.
class MarketIndex(Asset):
    
    def __init__(self, ticker: str, name: str, initial_value: float):
        super().__init__(ticker, name, initial_value)
        self._components: List[Asset] = []

    def add_component(self, asset: Asset) -> None:
        if asset not in self._components:
            self._components.append(asset)

    def get_asset_info(self) -> str:
        components_tickers = ", ".join([a.ticker for a in self._components])
        return (f"[Индекс] {self.name} ({self.ticker}). Значение: {self.price}. "
                f"Включает активы: {components_tickers or 'Нет'}")