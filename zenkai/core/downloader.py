import yt_dlp
import os
from typing import Optional, Callable, Dict
import logging

class StreamDownloader:
    def __init__(self, temp_dir: str = "downloads/temp"):
        self.temp_dir = temp_dir
        os.makedirs(self.temp_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def download_stream(
        self, 
        url: str, 
        format_id: str, 
        progress_callback: Optional[Callable[[Dict], None]] = None
    ) -> str:
        """
        Downloads a specific format/stream from the URL.
        Returns the path to the downloaded file.
        """
        output_template = os.path.join(self.temp_dir, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress_callback] if progress_callback else [],
            'overwrites': True, # Overwrite temp files if restarting
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # yt-dlp might download to a filename different from the template if it sanitizes chars
            # We can find the actual filename from the info dict or by preparing the filename
            filename = ydl.prepare_filename(info)
            return filename
