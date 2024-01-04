from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from server import app
from train import Train
import os

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"New file created: {event.src_path}")
        os.system("python server.py")

    def on_modified(self, event):
        print(f"File modified: {event.src_path}")
        os.system("python server.py")

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")
        os.system("python server.py")

if __name__ == "__main__":
    # Monitor the "similar_images" directory for changes
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path="C:/wamp64/www/fyp/goodgoods/public/uploads/similar_images", recursive=True)
    observer.start()

    # Start Flask app
    app.run("0.0.0.0", port=5000, debug=True)

    observer.stop()
