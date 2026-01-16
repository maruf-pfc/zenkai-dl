# zenkai-dl

A modular, developer-focused video download manager built for precision and control.

**zenkai-dl** is designed to be a robust tool that separates the core extraction logic from the user interface, allowing for maintainable and extensible video downloading capabilities.

## 🎯 Goals

- **Universal Support**: Detect video & audio streams from major platforms (YouTube, Vimeo, etc.).
- **Full Control**: Inspect available formats and choose specifically what to download (resolution, codec, container).
- **Smart Processing**: Automatically merge high-quality video and audio streams using FFmpeg.
- **Modular Design**: 
    - `zenkai-core`: Internal engine for logic, extraction, and processing.
    - `zenkai-dl`: User-facing CLI tool.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Extraction Engine**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Media Processing**: [FFmpeg](https://ffmpeg.org/)
- **Interface**: CLI (Command Line Interface), with future GUI support planned.

## 🏗️ Architecture

The project follows a strict separation of concerns:
- **Core**: Handles interactions with `yt-dlp`, temporary file management, and FFmpeg muxing.
- **CLI**: Handles arguments, configuration, and user feedback (progress bars, logs).

See [ARCHITECTURE.md](ARCHITECTURE.md) for a deep dive into the system design.

## ⚠️ Disclaimer

This project is for **educational and personal-use purposes only**. Users are responsible for complying with the terms of service of the websites they access.
