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
bg_music_path = f"{temp_dir_path}/bg_music.mp3"
font_name = "The Bold Font"

voices = {
    "grandpa": "NOpBlnGInO9m6vDvFkFC",
    "chris_brift": "UEKYgullGqaF0keqT8Bu"
}

def clean_up():
    shutil.rmtree(temp_dir_path)
    print(f"The directory '{temp_dir_path}' has been removed successfully.")

try:
    # Creates a temporary directory
    os.makedirs(temp_dir_path, exist_ok=True)

    # Initiate engines
    audio_engine = AudioEngine(temp_dir_path, voices['chris_brift'])
    video_engine = VideoEngine(temp_dir_path)
    story_engine = StoryEngine()
    youtube_engine = YoutubeEngine(output_video_file_path)
    
    # Joins existing video and creates an input video and puts it inside the temporary directory
    video_engine.generate_input_video()

    # # Creates a story based on the provided category
    story_result = story_engine.generate_story()
    story = story_result['story']
    story_title = story_result['title']

    # Converts the text story into audio and srt and stores them in the temporary directory
    timestamp = audio_engine.text_to_speech_and_timestamp(story, input_audio_file_path)
    audio_engine.timestamp_to_srt(timestamp, input_srt_file_path)
    audio_engine.download_bg_music()
    
    # # Combines the input video, audio and srt and generates a output video
    video_engine.generate_output_video(input_video_file_path, input_audio_file_path, input_srt_file_path, output_video_file_path, font_name, bg_music_path)
    
    # # Uploads the output video to YouTube
    youtube_engine.upload_video(story_title)
    
    clean_up()
except Exception as e:
    print('### ERROR OCCURRED')
    print(e)
    clean_up()
