import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            print(f'New image added: {event.src_path}')
            # You can add additional logic here if needed

if __name__ == "__main__":
    path = "images"
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
