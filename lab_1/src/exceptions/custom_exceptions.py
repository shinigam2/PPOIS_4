class ExchangeBaseException(Exception):
    """Базовый класс для всех исключений валютно-фондовой биржи."""
    pass


class InsufficientFundsError(ExchangeBaseException):
    """Исключение: недостаточно средств для проведения операции."""
    pass


class AssetNotFoundError(ExchangeBaseException):
    """Исключение: запрашиваемый актив (валюта/акция) не найден на бирже."""
    pass


class InvalidTransactionError(ExchangeBaseException):
    """Исключение: недопустимая транзакция (например, попытка купить 0 акций)."""
    pass


class AuthorizationError(ExchangeBaseException):
    """Исключение: ошибка доступа (например, трейдер не зарегистрирован у брокера)."""
    pass