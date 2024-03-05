from os.path import dirname, join

from pynput.keyboard import Key


START_KEY = Key.f10
KEEP_SEGMENT_KEY = Key.f11
DISCARD_SEGMENT_KEY = Key.f12
STOP_RECORDING_KEY = None

SEGMENTS_JSON_FILE_PATH = join(dirname(__file__), "segments.json")
