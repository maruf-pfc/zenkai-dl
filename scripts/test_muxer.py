from zenkai.core.muxer import StreamMuxer
import os
import subprocess

def create_dummy_files():
    # Create 1s red video
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=red:s=320x240:d=1', 
        '-c:v', 'libx264', 'dummy_video.mp4'
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Create 1s sine wave audio
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'sine=f=440:d=1', 
        '-c:a', 'aac', 'dummy_audio.m4a'
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return 'dummy_video.mp4', 'dummy_audio.m4a'

def main():
    muxer = StreamMuxer()
    output_file = "dummy_output.mp4"
    
    print("1. Creating dummy files...")
    v, a = create_dummy_files()
    
    print(f"2. Muxing {v} + {a} -> {output_file}...")
    try:
        res = muxer.mux_streams(v, a, output_file)
        print(f"Success! Output: {res}")
        print(f"Size: {os.path.getsize(res)} bytes")
        
        # Cleanup
        muxer.cleanup([v, a, output_file])
        print("Cleanup complete.")
        
    except Exception as e:
        print(f"Muxing failed: {e}")

if __name__ == "__main__":
    main()
