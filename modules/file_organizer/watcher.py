import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, organizer):
        self.organizer = organizer

    def on_created(self, event):
        if not event.is_directory:
            logging.info("New file detected, organizing...")
            time.sleep(1)
            self.organizer.organize()


class FolderWatcher:
    def __init__(self, path, organizer):
        self.path = path
        self.organizer = organizer
        self.observer = Observer()
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True
        event_handler = FolderEventHandler(self.organizer)
        self.observer.schedule(event_handler, self.path, recursive=False)
        self.observer.start()
        logging.info("Folder watcher started")

        while self.running:
            time.sleep(1)

        self.observer.stop()
        self.observer.join()
        logging.info("Folder watcher stopped")

    def stop(self):
        self.running = False
