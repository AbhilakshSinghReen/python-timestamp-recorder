from json import dump as json_dump, load as json_load
from os.path import dirname, join
from time import time

from pynput.keyboard import Key, Listener

from utils import convert_timestamp


START_KEY = Key.f10
KEEP_SEGMENT_KEY = Key.f11
DISCARD_SEGMENT_KEY = Key.f12


class TimestampRecorder:
    def __init__(self):
        self.segments_json_file_path = join(dirname(__file__), "segments.json")

        self.start_timestamp = None

    def add_segment_to_json_file(self, segment_type, timestamp):
        with open(self.segments_json_file_path, 'r') as segments_json_file:
            segments =  json_load(segments_json_file)

        if segment_type == "START" and len(segments) > 0:
            print("One or more segments already exist in the segments file. Cannot write a START segment. Exiting...")
            exit(1)

        first_segment = None
        last_segment = None
        if len(segments) > 0:
            first_segment = segments[0]
            last_segment = segments[-1]
        
        segments.append({
            'type': segment_type,
            'endTimestamp': timestamp,
        })

        with open(self.segments_json_file_path, 'w') as segments_json_file:
            json_dump(segments, segments_json_file, indent=4)
        
        if segment_type == "START":
            print(f"START timestamp has been recorded: {timestamp}")
            return

        if first_segment is None or last_segment is None:
            return
        
        segment_start_timestamp = last_segment['endTimestamp'] - first_segment['endTimestamp']
        segment_end_timestamp = timestamp - first_segment['endTimestamp']
        segment_duration = segment_end_timestamp - segment_start_timestamp

        segment_start_time_str = convert_timestamp(segment_start_timestamp)
        segment_end_time_str = convert_timestamp(segment_end_timestamp)
        segment_duration_str = convert_timestamp(segment_duration)
    
        if segment_type == "KEEP":
            print(f"Segment from {segment_start_time_str} to {segment_end_time_str} has been kept.")
        elif segment_type == "DISCARD":
            print(f"Segment from {segment_start_time_str} to {segment_end_time_str} has been discarded.")
        
        print(4 * " " + f"Segment duration: {segment_duration_str}")
    
    def on_release(self, key):
        event_timestamp = time()

        if self.start_timestamp is None and key != START_KEY:
            print("Please record the start timestamp before recording any other events.")
            return

        if key == START_KEY:
            if self.start_timestamp is not None:
                print("Start timestamp has already been recorded, ignoring this key press.")
                return
            
            self.start_timestamp = event_timestamp
            self.add_segment_to_json_file("START", event_timestamp)
        elif key == KEEP_SEGMENT_KEY:
            self.add_segment_to_json_file("KEEP", event_timestamp)
        elif key == DISCARD_SEGMENT_KEY:
            self.add_segment_to_json_file("DISCARD", event_timestamp)
        else:
            print(f"Key {key} is not configured for any operation.")
        
    def listen(self):
        with Listener(on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    timestamp_recorder = TimestampRecorder()
    timestamp_recorder.listen()
