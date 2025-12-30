from flask import Flask, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Define the output file path
    output_file = "test.jpg"
    
    # Remove existing file if present (optional, ensures latest capture)
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the rpicam-still command to capture the image
    try:
        subprocess.run(["rpicam-jpeg", "--output", output_file], check=True)
    except subprocess.CalledProcessError as e:
        return f"Error capturing image: {e}", 500

    return f"<img src='/image' alt='Raspberry Pi Image'>"

@app.route('/image')
def get_image():
    # Serve the captured image
    output_file = "test.jpg"
    if os.path.exists(output_file):
        return send_file(output_file, mimetype='image/jpeg')
    else:
        return "No image available. Please refresh the page.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
