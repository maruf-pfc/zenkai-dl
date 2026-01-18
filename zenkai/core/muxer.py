import ffmpeg
import os
import logging

class StreamMuxer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def mux_streams(self, video_path: str, audio_path: str, output_path: str) -> str:
        """
        Merges video and audio streams into a single file.
        Uses ffmpeg copy codec for speed.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        try:
            input_video = ffmpeg.input(video_path)
            input_audio = ffmpeg.input(audio_path)
            
            # Equivalent to: ffmpeg -i video -i audio -c copy output.mkv
            (
                ffmpeg
                .output(input_video, input_audio, output_path, c='copy', loglevel='error')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            return output_path
            
        except ffmpeg.Error as e:
            self.logger.error(f"FFmpeg error: {e.stderr.decode('utf8')}")
            raise RuntimeError(f"FFmpeg muxing failed: {e.stderr.decode('utf8')}")

    def cleanup(self, files: list[str]):
        """Removes temporary files."""
        for f in files:
            if os.path.exists(f):
                os.remove(f)
