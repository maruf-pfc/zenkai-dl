# Architecture: zenkai-dl

## 1. Overall System Design

**zenkai-dl** follows a modular "Core + Interface" architecture.

*   **zenkai-core**: The engine room. A pure Python library (package) that handles the heavy lifting—extraction, downloading, and processing. It knows *how* to download but doesn't care *who* is asking (CLI, GUI, or another script).
*   **zenkai-dl**: The commander. A CLI wrapper that parses user arguments, handles configuration, invokes `zenkai-core`, and displays progress bars and logs to the terminal.

### Advantages
*   **Testability**: Core logic can be tested without mocking stdin/stdout.
*   **Extensibility**: A future GUI (Step 13) can simply import `zenkai-core` without rewriting logic.
*   **Maintenance**: Tightly scoped responsibilities.

## 2. Data Flow

1.  **Input**: User provides a URL (and optional flags) to the CLI.
2.  **Extraction**: `zenkai-core` passes the URL to `yt-dlp`.
    *   *Result*: JSON metadata (title, formats, thumbnails).
3.  **Selection**:
    *   The system filters available formats based on user preference (e.g., "best video", "1080p", "audio only").
    *   User confirms selection (if interactive mode matches).
4.  **Download**:
    *   Video stream (e.g., `.mp4` video-only) and Audio stream (e.g., `.m4a` audio-only) are downloaded separately to temporary paths.
    *   *Reason*: High-quality streams on YouTube often separate audio and video.
5.  **Processing (Muxing)**:
    *   `FFmpeg` merges the temp video + temp audio into the final output file (container: MKV/MP4).
    *   Metadata (tags, thumbnails) is embedded.
6.  **Cleanup**: Temporary files are removed.
7.  **Output**: Final file placed in the user's download directory.

## 3. Technology Stack Rationale

### Python
*   **Why**: Massive ecosystem, excellent string/bytes handling, first-class support for `yt-dlp` (which is written in Python).

### yt-dlp
*   **Why**: The "Extraction Engine".
*   It handles the constant cat-and-mouse game of extraction (decrypting signatures, handling throttles).
*   We use it as a library, not just a subprocess command, for finer control.

### FFmpeg
*   **Why**: The "post-processor".
*   Unrivaled for muxing (merging) streams without re-encoding (stream copy), which is fast and preserves quality.
*   Handles format conversion if necessary.

## 4. Component Communication

*   **Internal**: Direct Python function calls.
    *   `zenkai.core.extractor.get_info(url)` -> returns `VideoMetadata` object.
    *   `zenkai.core.downloader.download(stream_id)` -> yields `Progress` events.
*   **External (CLI)**:
    *   The CLI subscribes to events (callbacks) from the Core to update the UI (Tqdm progress bars).
    *   Config files (YAML/TOML) inject settings into the Core context.

## Diagram (Text)

```mermaid
graph TD
    User[User] -->|CLI Command| Interface[zenkai-dl (CLI)]
    Interface -->|Config| ConfigLoader[Config System]
    Interface -->|URL| Extractor[zenkai-core: Extractor]
    Extractor -->|Uses| YTDLP[yt-dlp Library]
    YTDLP -->|Metadata| Extractor
    Extractor -->|List of Formats| Interface
    Interface -->|Selection| Downloader[zenkai-core: Downloader]
    Downloader -->|Video/Audio Streams| TempFiles[Temp Storage]
    TempFiles --> Processor[zenkai-core: Processor]
    Processor -->|Uses| FFmpeg[FFmpeg Binary]
    FFmpeg -->|Muxed File| FinalOutput[Final Output]
```
