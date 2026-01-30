# Douyin Watermark Remover

A web application that removes watermarks from Douyin (TikTok) videos by providing video links.

## Features

- 🎯 Remove bottom watermark from Douyin videos
- 🌐 Web interface for easy use
- 📱 API endpoint for programmatic access
- ⚡ Fast processing using optimized tools

## Technology Stack

- **Backend**: Python with Flask
- **Video Download**: yt-dlp
- **Video Processing**: FFmpeg
- **Frontend**: HTML/CSS/JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/douyin-watermark-remover.git
cd douyin-watermark-remover
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg:
```bash
# On Ubuntu/Debian
sudo apt-get install ffmpeg

# On macOS
brew install ffmpeg

# On Windows
# Download from https://ffmpeg.org/download.html
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and visit: `http://localhost:5000`

## Usage

1. Copy a Douyin video URL
2. Paste it in the input field
3. Click "Remove Watermark"
4. Download the processed video

## API Usage

```bash
curl -X POST http://localhost:5000/remove_watermark \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.douyin.com/video/1234567890"}'
```

## How It Works

1. **Download**: The application uses yt-dlp to download the Douyin video
2. **Process**: FFmpeg is used to crop the video, removing the bottom watermark area
3. **Return**: The processed video is returned for download

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.