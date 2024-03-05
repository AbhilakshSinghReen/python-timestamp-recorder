from datetime import timedelta


def convert_timestamp(seconds):
    time_format = str(timedelta(seconds=seconds))

    if '.' in time_format:
        time_format = time_format.split('.')[0]

    return time_format
