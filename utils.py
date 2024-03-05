from datetime import timedelta


def convert_timestamp(seconds):
    formatted_time = str(timedelta(seconds=seconds))

    milliseconds = int((seconds % 1) * 1000)

    if '.' in formatted_time:
        formatted_time = formatted_time.split('.')[0]
    
    formatted_time = f"{formatted_time}.{milliseconds:03d}"

    return formatted_time
