from flask import Flask, jsonify, send_from_directory, render_template
import os

app = Flask(__name__)
IMAGE_FOLDER = 'images'

@app.route('/images/<filename>')
def image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/api/images')
def list_images():
    files = os.listdir(IMAGE_FOLDER)
    images = [f for f in files if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
    return jsonify(images)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
