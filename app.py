from flask import Flask, jsonify, send_from_directory, render_template, request
from flask_socketio import SocketIO
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

app = Flask(__name__)
socketio = SocketIO(app)
IMAGE_FOLDER = 'images'


@app.route('/images/<setor>/<filename>')
def image(setor, filename):
    setor_path = os.path.join(IMAGE_FOLDER, setor)
    return send_from_directory(setor_path, filename)


@app.route('/api/images')
def list_images():
    setor = request.args.get('setor')
    if not setor:
        return jsonify({"error": "Setor não especificado"}), 400
    setor_path = os.path.join(IMAGE_FOLDER, setor)
    if not os.path.exists(setor_path):
        return jsonify({"error": "Setor não encontrado"}), 404
    files = os.listdir(setor_path)
    images = [f for f in files if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
    return jsonify(images)


@app.route('/')
def index():
    setor = request.args.get('setor')
    if not setor:
        return "Setor não especificado", 400
    return render_template('index.html', setor=setor)


class ImageHandler(FileSystemEventHandler):
    def __init__(self, setor):
        self.setor = setor

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            filename = os.path.basename(event.src_path)
            socketio.emit('new_image', {'filename': filename, 'setor': self.setor})
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            filename = os.path.basename(event.src_path)
            socketio.emit('delete_image', {'filename': filename, 'setor': self.setor})
    
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            filename = os.path.basename(event.src_path)
            socketio.emit('update_image', {'filename': filename, 'setor': self.setor})


def start_watching():
    observers = []
    for setor in os.listdir(IMAGE_FOLDER):
        setor_path = os.path.join(IMAGE_FOLDER, setor)
        if os.path.isdir(setor_path):
            event_handler = ImageHandler(setor=setor)
            observer = Observer()
            observer.schedule(event_handler, setor_path, recursive=False)
            observer.start()
            observers.append(observer)
    for observer in observers:
        observer.join()


if __name__ == '__main__':
    watcher_thread = threading.Thread(target=start_watching)
    watcher_thread.daemon = True
    watcher_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
