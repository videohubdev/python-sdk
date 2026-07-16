from .config import VideoHubConfig
from .http import HTTPClient
from .constants import WS_URL

from .services.auth import AuthService
from .services.rooms import RoomService
from .services.calls import CallService
from .services.admin import AdminService
from .attachments import AttachmentsAPI

from .ws import WSClient

import asyncio


class Client:

    def __init__(
        self,
        api_key: str,
        app_id: str,
        app_secret: str,
        app_platform: str,
        app_identifier: str,
        timeout: int = 10,
        app_name: str | None = None,
        domain: str | None = None,
        allow_video: bool = True,
        allow_audio: bool = True,
        allow_screen: bool = True,
        debug: bool = False,
    ):

        self.config = VideoHubConfig(
            api_key=api_key,
            app_id=app_id,
            app_secret=app_secret,
            app_platform=app_platform,
            app_identifier=app_identifier,
            timeout=timeout,
            app_name=app_name,
            domain=domain,
            allow_video=allow_video,
            allow_audio=allow_audio,
            allow_screen=allow_screen,
            debug=debug,
        )

        self.http = HTTPClient(self.config)

        self.auth = AuthService(self.http)
        self.rooms = RoomService(self.http)
        self.calls = CallService(self.http, self.config)
        self.admin = AdminService(self.http)
        self.attachments = AttachmentsAPI(self.http)
        self.rtc = WS_URL
        self.ws = WSClient(WS_URL)

    async def close(self):

        try:
            await self.http.close()
        except Exception:
            pass

        try:
            await self.ws.close()
        except Exception:
            pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.close())
        except:
            pass