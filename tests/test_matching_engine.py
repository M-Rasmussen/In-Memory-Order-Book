from src.matching_engine import MatchingEngine
from src.order import Order, Side


def test_buy_order_matches_existing_sell_order():
    engine = MatchingEngine()

    sell = Order(side=Side.SELL, price=100, quantity=5)
    engine.submit_order(sell)

    buy = Order(side=Side.BUY, price=105, quantity=5)
    trades = engine.submit_order(buy)

    assert len(trades) == 1
    assert trades[0].price == 100
    assert trades[0].quantity == 5


def test_order_does_not_match_when_prices_do_not_cross():
    engine = MatchingEngine()

    sell = Order(side=Side.SELL, price=110, quantity=5)
    engine.submit_order(sell)

    buy = Order(side=Side.BUY, price=100, quantity=5)
    trades = engine.submit_order(buy)

    assert len(trades) == 0
    assert engine.top_of_book()["best_bid"] == 100
    assert engine.top_of_book()["best_ask"] == 110


def test_partial_fill_leaves_remaining_quantity_on_book():
    engine = MatchingEngine()

    sell = Order(side=Side.SELL, price=100, quantity=10)
    engine.submit_order(sell)

    buy = Order(side=Side.BUY, price=100, quantity=4)
    trades = engine.submit_order(buy)

    assert len(trades) == 1
    assert trades[0].quantity == 4
    assert engine.top_of_book()["best_ask"] == 100
    assert engine.top_of_book()["ask_quantity"] == 6