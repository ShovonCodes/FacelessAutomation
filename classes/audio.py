import os
import json
import base64
import requests
from dotenv import load_dotenv
from classes.utils import convert_to_srt_time

load_dotenv()

api_key = os.getenv('ELEVENLABS_API_KEY')

class AudioEngine:
    def __init__(self, voice_id = 'NOpBlnGInO9m6vDvFkFC'):
        self.voice_id = voice_id
        
    def text_to_speech_and_timestamp(self, text, audio_path):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/with-timestamps"

        headers = {
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            print(f"Error encountered, status: {response.status_code}, "
                    f"content: {response.text}")
            quit()

        json_string = response.content.decode("utf-8")

        response_dict = json.loads(json_string)

        audio_bytes = base64.b64decode(response_dict["audio_base64"])

        with open(audio_path, 'wb') as f:
            f.write(audio_bytes)
            print('Story saved as MP3!')

        characters = response_dict['alignment']['characters']
        character_start_times_seconds = response_dict['alignment']['character_start_times_seconds']
        character_end_times_seconds = response_dict['alignment']['character_end_times_seconds']

        return {
            'characters': characters,
            'character_start_times_seconds': character_start_times_seconds,
            'character_end_times_seconds': character_end_times_seconds
            }

    def timestamp_to_srt(self, timestamp, srt_path):
        characters = timestamp['characters']
        character_start_times_seconds = timestamp['character_start_times_seconds']
        character_end_times_seconds = timestamp['character_end_times_seconds']
        
        words = []
        start_times = []
        end_times = []
        word = ""
        start_time = None
        end_time = None

        for i, char in enumerate(characters):
            if char not in [" ", ".", ",", '"']:
                word += char
                if start_time is None:
                    start_time = character_start_times_seconds[i]
                end_time = character_end_times_seconds[i]
            elif word:
                words.append(word)
                start_times.append(start_time)
                end_times.append(end_time)
                word = ""
                start_time = None
                end_time = None

        if word:
            words.append(word)
            start_times.append(start_time)
            end_times.append(end_time)

        srt_content = ""
        for i, word in enumerate(words):
            start_time_str = convert_to_srt_time(start_times[i])
            end_time_str = convert_to_srt_time(end_times[i])
            srt_content += f"{i+1}\n{start_time_str} --> {end_time_str}\n{word}\n\n"

        with open(srt_path, "w") as file:
            file.write(srt_content)
            print('Subtitle saved as SRT!')
