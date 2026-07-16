import json
import websockets


class WSClient:

    def __init__(self, url: str):
        self.url = url
        self.ws = None

    async def connect(self, token: str):
        self.ws = await websockets.connect(f"{self.url}?token={token}")

    async def send(self, data: dict):
        if not self.ws:
            raise RuntimeError("WebSocket not connected")

        await self.ws.send(json.dumps(data))

    async def receive(self):
        if not self.ws:
            raise RuntimeError("WebSocket not connected")

        msg = await self.ws.recv()
        return json.loads(msg)

    async def close(self):
        if self.ws:
            await self.ws.close()
            self.ws = None