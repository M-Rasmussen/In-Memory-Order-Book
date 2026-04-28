import heapq
from typing import Optional

from src.order import Order, Side


class OrderBook:
    def __init__(self):
        self.bids: list[Order] = []
        self.asks: list[Order] = []

    def add_order(self, order: Order) -> None:
        if order.side == Side.BUY:
            heapq.heappush(self.bids, order)
        elif order.side == Side.SELL:
            heapq.heappush(self.asks, order)
        else:
            raise ValueError("Invalid order side")

    def best_bid(self) -> Optional[Order]:
        return self.bids[0] if self.bids else None

    def best_ask(self) -> Optional[Order]:
        return self.asks[0] if self.asks else None

    def remove_best_bid(self) -> Order:
        return heapq.heappop(self.bids)

    def remove_best_ask(self) -> Order:
        return heapq.heappop(self.asks)

    def top_of_book(self) -> dict:
        best_bid = self.best_bid()
        best_ask = self.best_ask()

        return {
            "best_bid": best_bid.price if best_bid else None,
            "best_ask": best_ask.price if best_ask else None,
            "bid_quantity": best_bid.quantity if best_bid else None,
            "ask_quantity": best_ask.quantity if best_ask else None,
        }