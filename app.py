from flask import Flask, jsonify, send_from_directory, render_template
from flask_socketio import SocketIO
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

app = Flask(__name__)
socketio = SocketIO(app)
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

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            filename = os.path.basename(event.src_path)
            socketio.emit('new_image', {'filename': filename})

def start_watching():
    path = IMAGE_FOLDER
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    observer.join()

if __name__ == '__main__':
    watcher_thread = threading.Thread(target=start_watching)
    watcher_thread.daemon = True
    watcher_thread.start()
    socketio.run(app, debug=True)
