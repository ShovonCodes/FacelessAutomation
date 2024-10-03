import random
from datetime import timedelta

def convert_to_srt_time(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = int((td.microseconds) / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def pick_random(items):
    return random.choice(items)
