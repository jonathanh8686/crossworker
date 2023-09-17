import asyncio
from loguru import logger
from typing import Any, Callable
from websockets.client import WebSocketClientProtocol, connect


class WebsocketClient:
    HEARTBEAT_DELAY = 2
    RECV_TIMEOUT = 5
    LISTEN_DELAY = 1

    def __init__(self) -> None:
        self.messages: list[str] = []
        self.game_running = False

    async def heartbeat(self, client: WebSocketClientProtocol) -> None:
        while self.game_running:
            logger.info("Emitting heartbeat...")
            await client.send("2")
            await asyncio.sleep(self.HEARTBEAT_DELAY)

    async def listen(
        self, client: WebSocketClientProtocol, callback: Callable[[str], Any]
    ) -> None:
        while self.game_running:
            recv_data = await asyncio.wait_for(
                client.recv(), self.RECV_TIMEOUT
            )
            assert isinstance(recv_data, str)

            if recv_data != "":
                logger.info(
                    f"Recieved message from socket server: {recv_data}"
                )
                self.messages.append(recv_data)
                asyncio.create_task(callback(recv_data))

    async def join_game(
        self, game_id: str, callback: Callable[[str], Any]
    ) -> None:
        ws_url = "wss://api.foracross.com/socket.io/?EIO=3&transport=websocket"
        async with connect(ws_url) as client:
            logger.success("Successfully connected to WebSocket server")
            self.game_running = True
            heartbeat_task = asyncio.create_task(self.heartbeat(client))
            listen_task = asyncio.create_task(self.listen(client, callback))

            await client.send(f'420["join_game", "{game_id}"]')
            await client.send(f'421["sync_all_game_events", "{game_id}"]')

            await heartbeat_task
            await listen_task
