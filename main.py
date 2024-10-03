import os
import shutil
from classes.story import StoryEngine
from classes.video import VideoEngine
from classes.audio import AudioEngine
from classes.youtube import YoutubeEngine

temp_dir_path = 'tmp'
input_video_file_path = f"{temp_dir_path}/input_video.mp4"
input_audio_file_path = f"{temp_dir_path}/input_audio.mp3"
input_srt_file_path = f"{temp_dir_path}/input_srt.srt"
output_video_file_path = f"{temp_dir_path}/output_video.mp4"
font_name = "The Bold Font"

voices = {
    "grandpa": "NOpBlnGInO9m6vDvFkFC"
}

def clean_up():
    shutil.rmtree(temp_dir_path)
    print(f"The directory '{temp_dir_path}' has been removed successfully.")

try:
    # Creates a temporary directory
    os.makedirs(temp_dir_path, exist_ok=True)

    # Initiate engines
    audio_engine = AudioEngine(voices['grandpa'])
    video_engine = VideoEngine('materials/motivation', temp_dir_path)
    story_engine = StoryEngine()
    youtube_engine = YoutubeEngine(output_video_file_path)
    
    # Joins existing video and creates an input video and puts it inside the temporary directory
    video_engine.generate_input_video_temp()

    # # Creates a story based on the provided category
    # story = story_engine.generate_story()
    # # story = "This should give you the desired result where the video runs for 1 second longer than the audio"

    # # Converts the text story into audio and srt and stores them in the temporary directory
    # timestamp = audio_engine.text_to_speech_and_timestamp(story, input_audio_file_path)
    # audio_engine.timestamp_to_srt(timestamp, input_srt_file_path)
    
    # # Combines the input video, audio and srt and generates a output video
    # video_engine.generate_output_video(input_video_file_path, input_audio_file_path, input_srt_file_path, output_video_file_path, font_name)
    
    # # Uploads the output video to YouTube
    # youtube_engine.upload_video('First automated video! #shorts #motivation #ai', 'Subscribe to this channel for more videos like this!')
    
    clean_up()
except Exception as e:
    print('### ERROR OCCURRED')
    print(e)
    clean_up()
