from src.order import Order, Side
from src.order_book import OrderBook


def test_best_bid_returns_highest_buy_price():
    book = OrderBook()

    book.add_order(Order(side=Side.BUY, price=100, quantity=5))
    book.add_order(Order(side=Side.BUY, price=105, quantity=5))
    book.add_order(Order(side=Side.BUY, price=99, quantity=5))

    assert book.best_bid().price == 105


def test_best_ask_returns_lowest_sell_price():
    book = OrderBook()

    book.add_order(Order(side=Side.SELL, price=110, quantity=5))
    book.add_order(Order(side=Side.SELL, price=108, quantity=5))
    book.add_order(Order(side=Side.SELL, price=115, quantity=5))

    assert book.best_ask().price == 108