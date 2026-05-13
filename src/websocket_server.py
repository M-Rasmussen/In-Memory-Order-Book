import asyncio
import json
import os
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
        clients.discard(client)


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
        clients.discard(websocket)


async def main():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8765"))

    async with websockets.serve(handle_client, host, port):
        print(f"WebSocket server running on ws://{host}:{port}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
