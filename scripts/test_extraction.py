from zenkai.core.extractor import VideoExtractor
import json

def main():
    extractor = VideoExtractor()
    # Big Buck Bunny 30fps by Blender Foundation
    url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ" 
    
    print(f"Extracting info for {url}...")
    try:
        metadata = extractor.get_info(url)
        print(f"Title: {metadata.title}")
        print(f"Duration: {metadata.duration}s")
        print(f"Found {len(metadata.streams)} streams.")
        
        # Print first 3 streams
        for i, s in enumerate(metadata.streams[:3]):
            print(f"Stream {i}: {s.id} ({s.ext}) - {s.resolution}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
