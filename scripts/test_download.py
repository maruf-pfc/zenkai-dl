from zenkai.core.extractor import VideoExtractor
from zenkai.core.downloader import StreamDownloader
import os

def progress_hook(d):
    if d['status'] == 'downloading':
        pass
    elif d['status'] == 'finished':
        print("\nDownload complete!")

def main():
    extractor = VideoExtractor()
    downloader = StreamDownloader()
    
    # Big Buck Bunny (reliable)
    url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    
    print(f"1. Fetching info for {url}...")
    metadata = extractor.get_info(url)
    
    # Find list of mp4 streams
    mp4_streams = [s for s in metadata.streams if s.ext == 'mp4' and s.resolution]
    
    if not mp4_streams:
        print("No MP4 streams found.")
        return

    target_stream = mp4_streams[0]
    for s in mp4_streams:
        if '144p' in s.resolution or '240p' in s.resolution:
            target_stream = s
            break
            
    print(f"2. Downloading stream {target_stream.id} ({target_stream.resolution})...")
    try:
        fpath = downloader.download_stream(url, target_stream.id, progress_hook)
        print(f"Success! File saved to: {fpath}")
        if os.path.exists(fpath):
             print(f"File size: {os.path.getsize(fpath)} bytes")
        
    except Exception as e:
        print(f"Download failed: {e}")

if __name__ == "__main__":
    main()
