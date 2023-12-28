import asyncio
import threading
from websocket.websocket import start_websocket_server
from webserver.server import start_http_server


async def run_servers():
    websocket_thread = threading.Thread(target=lambda: asyncio.run(start_websocket_server()))
    websocket_thread.start()

    start_http_server()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_servers())