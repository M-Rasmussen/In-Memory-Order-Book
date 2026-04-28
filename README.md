# Order Book Matching Engine

## Overview
A simplified in-memory trading engine that models core exchange infrastructure, including order matching, trade execution, and real-time market data updates.

## Features
- Price-time priority matching
- Heap-based bid/ask order book
- Partial fill support
- Real-time WebSocket market data feed
- Unit tests for core matching behavior

## Tech Stack
- Python
- asyncio
- websockets
- pytest

## How to Run
pip install -r requirements.txt
python -m src.websocket_server

## Run Tests
pytest

## Future Improvements
- Add Redis-backed state
- Add message queue support
- Add latency benchmarking
- Add REST API for order submission
- Improve concurrency handling

## License
MIT