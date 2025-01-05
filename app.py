from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Path to the folder where your videos are stored
VIDEO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'videos')


@app.route('/')
def index():
    """List all .mp4 files in the video directory."""
    try:
        video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
    except FileNotFoundError:
        video_files = []
    return render_template('index.html', video_files=video_files)


@app.route('/videos/<filename>')
def serve_video(filename):
    """Serve the requested video file."""
    return send_from_directory(VIDEO_DIR, filename)


if __name__ == '__main__':
    # Ensure the video directory exists
    os.makedirs(VIDEO_DIR, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=8123)