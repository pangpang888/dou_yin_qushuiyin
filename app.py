from flask import Flask, request, render_template, send_file, jsonify
import os
import uuid
import subprocess
import requests
from urllib.parse import urlparse
import yt_dlp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def download_douyin_video(url):
    """Download Douyin video using yt-dlp"""
    video_id = str(uuid.uuid4())
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{video_id}.mp4")
    
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Check if file was created
        if not os.path.exists(output_path):
            # Try to find the downloaded file (yt-dlp might add extension)
            files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.startswith(video_id)]
            if files:
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], files[0])
        
        return output_path
    except Exception as e:
        print(f"Download error: {e}")
        return None

def remove_watermark(input_path, output_path):
    """Remove watermark using ffmpeg"""
    try:
        # Simple approach: crop the video to remove bottom watermark area
        # This is a basic method - more advanced watermark removal would require image analysis
        crop_command = [
            'ffmpeg',
            '-i', input_path,
            '-vf', 'crop=in_w:in_h-80',  # Crop 80 pixels from bottom
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        subprocess.run(crop_command, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_watermark', methods=['POST'])
def remove_watermark_api():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Validate URL
    try:
        result = urlparse(video_url)
        if not all([result.scheme, result.netloc]):
            return jsonify({'error': 'Invalid URL'}), 400
    except:
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # Download video
    input_path = download_douyin_video(video_url)
    if not input_path:
        return jsonify({'error': 'Failed to download video'}), 500
    
    # Remove watermark
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"processed_{uuid.uuid4()}.mp4")
    success = remove_watermark(input_path, output_path)
    
    # Clean up input file
    if os.path.exists(input_path):
        os.remove(input_path)
    
    if not success:
        if os.path.exists(output_path):
            os.remove(output_path)
        return jsonify({'error': 'Failed to process video'}), 500
    
    return send_file(output_path, as_attachment=True, download_name='video_no_watermark.mp4')

if __name__ == '__main__':
    app.run(debug=True)