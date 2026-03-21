from abc import ABC
from typing import List, Optional

from src.core.portfolio import Portfolio
from src.exceptions.custom_exceptions import AuthorizationError


class Participant(ABC):
    """
    Базовый абстрактный класс для участников биржи.
    """
    def __init__(self, name: str):
        self.name = name
        # Композиция: каждый участник имеет свой портфель
        self.portfolio = Portfolio()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.name}"


class Broker(Participant):
    """
    Брокер, предоставляющий доступ к бирже для трейдеров.
    Может взимать комиссию за сделки.
    """
    def __init__(self, name: str, commission_rate: float = 0.01):
        super().__init__(name)
        self.commission_rate = commission_rate
        self._registered_traders: List['Trader'] = []

    def register_trader(self, trader: 'Trader') -> None:
        """Регистрация трейдера у брокера."""
        if trader not in self._registered_traders:
            self._registered_traders.append(trader)
            trader.set_broker(self)

    def is_trader_registered(self, trader: 'Trader') -> bool:
        """Проверка, обслуживается ли трейдер данным брокером."""
        return trader in self._registered_traders


class Trader(Participant):
    """
    Трейдер, осуществляющий торговлю активами через брокера.
    """
    def __init__(self, name: str):
        super().__init__(name)
        self._broker: Optional[Broker] = None

    def set_broker(self, broker: Broker) -> None:
        """Привязывает трейдера к брокеру (вызывается самим брокером при регистрации)."""
        self._broker = broker

    def get_broker(self) -> Broker:
        """Возвращает брокера трейдера или вызывает ошибку, если его нет."""
        if not self._broker:
            raise AuthorizationError(f"Трейдер {self.name} не зарегистрирован у брокера.")
        return self._broker