import asyncio
from loguru import logger
from websockets.client import WebSocketClientProtocol, connect


class WebsocketClient:
    HEARTBEAT_DELAY = 2
    RECV_TIMEOUT = 5
    LISTEN_DELAY = 1

    def __init__(self) -> None:
        self.messages: list[str] = []

    async def heartbeat(self, client: WebSocketClientProtocol) -> None:
        while True:
            logger.info("Emitting heartbeat...")
            await client.send("2")
            await asyncio.sleep(self.HEARTBEAT_DELAY)

    async def listen(self, client: WebSocketClientProtocol) -> None:
        while True:
            recv_data = await asyncio.wait_for(
                client.recv(), self.RECV_TIMEOUT
            )
            recv_data = await client.recv()
            assert isinstance(recv_data, str)

            if recv_data != "":
                logger.info(
                    f"Recieved message from socket server: {recv_data}"
                )
                self.messages.append(recv_data)

            with open("test.dat", "w") as f:
                f.write("\n".join(self.messages))

    async def join_game(self, game_id: str) -> None:
        ws_url = "wss://api.foracross.com/socket.io/?EIO=3&transport=websocket"
        async with connect(ws_url) as client:
            logger.success("Successfully connected to WebSocket server")
            heartbeat_task = asyncio.create_task(self.heartbeat(client))
            await client.send(f'420["join_game", "{game_id}"]')
            await client.send(f'421["sync_all_game_events", "{game_id}"]')

            listen_task = asyncio.create_task(self.listen(client))

            await heartbeat_task
            await listen_task
