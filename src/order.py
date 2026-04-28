from dataclasses import dataclass, field
from enum import Enum
import time
import uuid


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass(order=True)
class Order:
    sort_index: tuple = field(init=False, repr=False)
    side: Side
    price: float
    quantity: int
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if self.price <= 0:
            raise ValueError("Price must be greater than 0")

        if self.side == Side.BUY:
            self.sort_index = (-self.price, self.timestamp)
        else:
            self.sort_index = (self.price, self.timestamp)