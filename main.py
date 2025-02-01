import os
import json
import shutil
import argparse
from classes.story import StoryEngine
from classes.video import VideoEngine
from classes.audio import AudioEngine
from classes.youtube import YoutubeEngine

def load_config(channel_name):
    with open('channel_config.json', 'r') as f:
        config = json.load(f)
    return config.get(channel_name)

# Common values
temp_dir_path = 'tmp'
input_video_file_path = f"{temp_dir_path}/input_video.mp4"
input_audio_file_path = f"{temp_dir_path}/input_audio.mp3"
input_srt_file_path = f"{temp_dir_path}/input_srt.srt"
output_video_file_path = f"{temp_dir_path}/output_video.mp4"
bg_music_path = f"{temp_dir_path}/bg_music.mp3"


def clean_up():
    shutil.rmtree(temp_dir_path)
    print(f"The directory '{temp_dir_path}' has been removed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run YouTube automation for a specific channel.')
    parser.add_argument('channel_name', type=str, help='The name of the channel to run the automation for.')
    args = parser.parse_args()

    channel_config = load_config(args.channel_name)
    if not channel_config:
        print(f"Configuration for channel '{args.channel_name}' not found.")
        exit(1)

    # Extract values from json
    channel_refresh_token_key = channel_config['channel_refresh_token_key']
    asset_directory = channel_config['asset_directory']
    voice = channel_config['voice']
    topics = channel_config['topics']
    prompt_styles = channel_config['prompt_styles']
    guidelines = channel_config['guidelines']
    system_message = channel_config['system_message']
    video_description = channel_config['video_description']
    video_tags = channel_config['video_tags']

    try:
        # Creates a temporary directory
        os.makedirs(temp_dir_path, exist_ok=True)

        # Initiate engines
        video_engine = VideoEngine(asset_directory, temp_dir_path)
        story_engine = StoryEngine(
            topics=topics,
            prompt_styles=prompt_styles,
            guidelines=guidelines,
            system_message=system_message
        )
        
        audio_engine = AudioEngine(temp_dir_path, voice)
        youtube_engine = YoutubeEngine(
            video_file_path=output_video_file_path,
            refresh_token_key=channel_refresh_token_key,
            tags=video_tags,
            description=video_description
        )
        
        # Joins existing video and creates an input video and puts it inside the temporary directory
        video_engine.generate_input_video()

        # Creates a story based on the provided category
        story_result = story_engine.generate_story()
        story = story_result['story']
        story_title = story_result['title']

        # # Converts the text story into audio and srt and stores them in the temporary directory
        timestamp = audio_engine.text_to_speech_and_timestamp(story, input_audio_file_path)
        audio_engine.timestamp_to_srt(timestamp, input_srt_file_path)
        
        # # # Combines the input video, audio and srt and generates a output video
        video_engine.generate_output_video(input_video_file_path, input_audio_file_path, input_srt_file_path, output_video_file_path)
        
        # # # Uploads the output video to YouTube
        youtube_engine.upload_video(story_title)
        
        clean_up()
    except Exception as e:
        print('### ERROR OCCURRED')
        print(e)
        clean_up()
