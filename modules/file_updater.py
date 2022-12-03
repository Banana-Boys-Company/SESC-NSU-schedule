from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
import time


class Handler(PatternMatchingEventHandler):
    def on_created(self, event):
        print(event)

    def on_deleted(self, event):
        print(event)

    def on_moved(self, event):
        print(event)


event_handler = Handler(
    patterns=['*.jpg', '*.png', '*.gif', '*.webm', '*.jpeg'],
    ignore_patterns=[],
    ignore_directories=True,
    case_sensitive=False
)

observer = Observer()
observer.schedule(Handler(), path='static/images/banner/', recursive=True)
observer.start()


def main():
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def setup():
    main()
