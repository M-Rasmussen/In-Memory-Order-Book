import asyncio
import json
import websockets


async def send_order(side: str, price: float, quantity: int):
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        order = {
            "side": side,
            "price": price,
            "quantity": quantity,
        }

        await websocket.send(json.dumps(order))

        response = await websocket.recv()
        print(json.dumps(json.loads(response), indent=2))


if __name__ == "__main__":
    asyncio.run(send_order("buy", 100.00, 10))