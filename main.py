from json import dump as json_dump, load as json_load
from time import time

from pynput.keyboard import Key, Listener


START_KEY = Key.f10
KEEP_SEGMENT_KEY = Key.f11
DISCARD_SEGMENT_KEY = Key.f12


class TimestampRecorder:
    def __init__(self):
        self.start_timestamp = None
    
    def on_release(self, key):
        print('{0} release'.format(key))
        if key == Key.esc:
            return False
    
    def listen(self):
        with Listener(on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    timestamp_recorder = TimestampRecorder()
    timestamp_recorder.listen()
