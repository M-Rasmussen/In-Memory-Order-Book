import asyncio
import json
from dataclasses import asdict

import websockets

from src.matching_engine import MatchingEngine
from src.order import Order, Side


engine = MatchingEngine()
clients = set()


async def broadcast(message: dict) -> None:
    if not clients:
        return

    payload = json.dumps(message)

    disconnected = []

    for client in clients:
        try:
            await client.send(payload)
        except websockets.exceptions.ConnectionClosed:
            disconnected.append(client)

    for client in disconnected:
        clients.remove(client)


async def handle_client(websocket):
    clients.add(websocket)

    try:
        async for message in websocket:
            data = json.loads(message)

            order = Order(
                side=Side(data["side"]),
                price=float(data["price"]),
                quantity=int(data["quantity"]),
            )

            trades = engine.submit_order(order)

            response = {
                "event": "order_update",
                "order_id": order.order_id,
                "trades": [asdict(trade) for trade in trades],
                "top_of_book": engine.top_of_book(),
            }

            await broadcast(response)

    except Exception as error:
        await websocket.send(
            json.dumps(
                {
                    "event": "error",
                    "message": str(error),
                }
            )
        )

    finally:
        clients.remove(websocket)


async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())