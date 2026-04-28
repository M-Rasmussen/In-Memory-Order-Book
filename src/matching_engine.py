from dataclasses import dataclass
from typing import List

from src.order import Order, Side
from src.order_book import OrderBook


@dataclass
class Trade:
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: int


class MatchingEngine:
    def __init__(self):
        self.order_book = OrderBook()

    def submit_order(self, order: Order) -> List[Trade]:
        if order.side == Side.BUY:
            return self._match_buy(order)

        if order.side == Side.SELL:
            return self._match_sell(order)

        raise ValueError("Invalid order side")

    def _match_buy(self, buy_order: Order) -> List[Trade]:
        trades = []

        while buy_order.quantity > 0:
            best_ask = self.order_book.best_ask()

            if best_ask is None or best_ask.price > buy_order.price:
                break

            trade_quantity = min(buy_order.quantity, best_ask.quantity)

            trades.append(
                Trade(
                    buy_order_id=buy_order.order_id,
                    sell_order_id=best_ask.order_id,
                    price=best_ask.price,
                    quantity=trade_quantity,
                )
            )

            buy_order.quantity -= trade_quantity
            best_ask.quantity -= trade_quantity

            if best_ask.quantity == 0:
                self.order_book.remove_best_ask()

        if buy_order.quantity > 0:
            self.order_book.add_order(buy_order)

        return trades

    def _match_sell(self, sell_order: Order) -> List[Trade]:
        trades = []

        while sell_order.quantity > 0:
            best_bid = self.order_book.best_bid()

            if best_bid is None or best_bid.price < sell_order.price:
                break

            trade_quantity = min(sell_order.quantity, best_bid.quantity)

            trades.append(
                Trade(
                    buy_order_id=best_bid.order_id,
                    sell_order_id=sell_order.order_id,
                    price=best_bid.price,
                    quantity=trade_quantity,
                )
            )

            sell_order.quantity -= trade_quantity
            best_bid.quantity -= trade_quantity

            if best_bid.quantity == 0:
                self.order_book.remove_best_bid()

        if sell_order.quantity > 0:
            self.order_book.add_order(sell_order)

        return trades

    def top_of_book(self) -> dict:
        return self.order_book.top_of_book()