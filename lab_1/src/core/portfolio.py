from typing import Dict
from src.exceptions.custom_exceptions import InsufficientFundsError


class Portfolio:
    """
    Класс для управления активами участника торгов.
    Хранит балансы валют и акций.
    """

    def __init__(self):
        # Словарь для хранения балансов активов: {тикер: количество}
        self._balances: Dict[str, float] = {}

    def deposit(self, ticker: str, amount: float) -> None:
        """Пополнение баланса конкретного актива."""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля.")
        
        # Если актива еще нет, get вернет 0.0, и мы прибавим amount
        self._balances[ticker] = self._balances.get(ticker, 0.0) + amount

    def withdraw(self, ticker: str, amount: float) -> None:
        """Списание актива с баланса."""
        if amount <= 0:
            raise ValueError("Сумма списания должна быть больше нуля.")
        
        if ticker not in self._balances or self._balances[ticker] < amount:
            raise InsufficientFundsError(f"Недостаточно средств для актива '{ticker}'.")
            
        self._balances[ticker] -= amount
        
        # Очистка нулевых балансов для порядка
        if self._balances[ticker] == 0:
            del self._balances[ticker]

    def get_balance(self, ticker: str) -> float:
        """Возвращает текущий баланс по тикеру актива."""
        return self._balances.get(ticker, 0.0)

    def get_all_balances(self) -> Dict[str, float]:
        """Возвращает копию всех балансов."""
        return self._balances.copy()