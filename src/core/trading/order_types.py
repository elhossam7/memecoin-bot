from enum import Enum

class OrderTypes(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    FLASH_LOAN = "flash_loan"
    ARBITRAGE = "arbitrage"

__all__ = ['OrderTypes']

class OrderType:
    def __init__(self, order_type, price=None, quantity=None):
        self.order_type = order_type
        self.price = price
        self.quantity = quantity

class MarketOrder(OrderType):
    def __init__(self, quantity):
        super().__init__('market', quantity=quantity)

class LimitOrder(OrderType):
    def __init__(self, price, quantity):
        super().__init__('limit', price=price, quantity=quantity)

class StopLossOrder(OrderType):
    def __init__(self, price, quantity):
        super().__init__('stop-loss', price=price, quantity=quantity)

class TakeProfitOrder(OrderType):
    def __init__(self, price, quantity):
        super().__init__('take-profit', price=price, quantity=quantity)