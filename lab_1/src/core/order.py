from enum import Enum
from src.core.participant import Trader
from src.utils.descriptor import ValidatedNumber


class OrderType(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Order:
    
    # Количество и цена не могут быть отрицательными или нулевыми
    amount = ValidatedNumber(min_value=0, allow_zero=False)
    price = ValidatedNumber(min_value=0, allow_zero=False)

    def __init__(self, trader: Trader, order_type: OrderType, ticker: str, amount: float, price: float):
        self.trader = trader
        self.order_type = order_type
        self.ticker = ticker
        self.amount = amount
        self.price = price

    # Возвращает общую стоимость заявки (сумма сделки).
    def get_total_value(self) -> float:
        return self.amount * self.price

    def __str__(self) -> str:
        operation = "Покупка" if self.order_type == OrderType.BUY else "Продажа"
        return (f"Заявка от {self.trader.name}: {operation} {self.amount} шт. "
                f"актива '{self.ticker}' по цене {self.price}")