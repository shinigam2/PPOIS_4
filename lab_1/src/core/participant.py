from abc import ABC
from typing import List, Optional

from src.core.portfolio import Portfolio
from src.exceptions.custom_exceptions import AuthorizationError


class Participant(ABC):
    def __init__(self, name: str):
        self.name = name
        # каждый участник имеет свой портфель
        self.portfolio = Portfolio()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.name}"


class Broker(Participant):

    def __init__(self, name: str, commission_rate: float = 0.01):
        super().__init__(name)
        self.commission_rate = commission_rate
        self._registered_traders: List['Trader'] = []

    def register_trader(self, trader: 'Trader') -> None:
        if trader not in self._registered_traders:
            self._registered_traders.append(trader)
            trader.set_broker(self)

    def is_trader_registered(self, trader: 'Trader') -> bool:
        return trader in self._registered_traders


class Trader(Participant):

    def __init__(self, name: str):
        super().__init__(name)
        self._broker: Optional[Broker] = None
    # Привязывает трейдера к брокеру
    def set_broker(self, broker: Broker) -> None:
        self._broker = broker

    def get_broker(self) -> Broker:
        if not self._broker:
            raise AuthorizationError(f"Трейдер {self.name} не зарегистрирован у брокера.")
        return self._broker