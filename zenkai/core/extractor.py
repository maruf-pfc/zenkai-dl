import yt_dlp
from typing import List, Dict, Any
from .models import VideoMetadata, StreamInfo

class VideoExtractor:
    def __init__(self):
        self._ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,  # We need full info
        }

    def get_info(self, url: str) -> VideoMetadata:
        """
        Extracts metadata and available formats for a given URL.
        """
        with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return self._parse_info(info, url)

    def _parse_info(self, info: Dict[str, Any], url: str) -> VideoMetadata:
        formats = info.get('formats', [])
        streams: List[StreamInfo] = []

        for f in formats:
            # Skip formats without streams (e.g. m3u8 manifests if redundant)
            if not f.get('url'):
                continue
            
            # Simple filtering logic can be expanded
            streams.append(StreamInfo(
                id=f['format_id'],
                ext=f.get('ext', 'unknown'),
                resolution=f.get('resolution'),
                filesize=f.get('filesize'),
                tbr=f.get('tbr'),
                fps=f.get('fps'),
                vcodec=f.get('vcodec', 'none'),
                acodec=f.get('acodec', 'none'),
                note=f.get('format_note')
            ))

        return VideoMetadata(
            id=info['id'],
            title=info['title'],
            uploader=info.get('uploader', 'Unknown'),
            duration=int(info.get('duration', 0)),
            thumbnail=info.get('thumbnail', ''),
            original_url=url,
            streams=streams
        )
