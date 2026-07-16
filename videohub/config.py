from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoHubConfig:

    api_key: str
    app_id: str
    app_secret: str
    app_platform: str
    app_identifier: str

    timeout: int = 10

    app_name: Optional[str] = None
    domain: Optional[str] = None

    allow_video: bool = True
    allow_audio: bool = True
    allow_screen: bool = True

    debug: bool = False