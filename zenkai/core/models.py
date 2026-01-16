from typing import List, Optional
from pydantic import BaseModel

class StreamInfo(BaseModel):
    id: str
    ext: str
    resolution: Optional[str] = None
    filesize: Optional[int] = None
    tbr: Optional[float] = None  # Total bitrate
    fps: Optional[float] = None
    vcodec: str
    acodec: str
    note: Optional[str] = None  # e.g., "1080p video only"

class VideoMetadata(BaseModel):
    id: str
    title: str
    uploader: str
    duration: int
    thumbnail: str
    original_url: str
    streams: List[StreamInfo]
