import os
import math
import random
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

github_access_token = os.getenv('GHUB_ACCESS_TOKEN')

def count_files_in_github_directory(path):
    owner = "ShovonCodes"
    repo = "assets"

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    if github_access_token:
        headers["Authorization"] = f"Bearer {github_access_token}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP issues

        contents = response.json()
        if isinstance(contents, list):
            files = [item for item in contents if item['type'] == 'file']
            return len(files)
        else:
            print("Specified path is not a directory or doesn't exist.")
            return 0

    except requests.exceptions.RequestException as e:
        print(f"Error fetching directory contents: {e}")
        return 0

class VideoEngine:
    def __init__(self, asset_dir, temp_dir = 'tmp'):
        self.temp_dir = temp_dir
        self.asset_dir = asset_dir

    def select_random_videos(self, count):
        file_count = count_files_in_github_directory(self.asset_dir)
        if file_count < count:
            print(f"Insufficient videos available. Requested: {count}, Available: {file_count}")
            return []
        
        video_urls = [f"http://raw.githubusercontent.com/ShovonCodes/assets/master/{self.asset_dir}/{i+1}.mp4" for i in range(file_count)]
        return random.sample(video_urls, count)

    def download_videos(self, urls):
        # Create the output folder if it doesn't exist
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        file_paths = []
        for idx, url in enumerate(urls):
            video_name = f"video_{idx + 1}.mp4"
            absolute_path = os.path.abspath(f"{self.temp_dir}/{video_name}")
            print(f"Downloading {url}...")

            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(absolute_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            file_paths.append(absolute_path)

        return file_paths

    def generate_file_list(self, file_paths, txt_file="files.txt"):
        with open(f'{self.temp_dir}/{txt_file}', 'w') as f:
            for file_path in file_paths:
                f.write(f"file '{file_path}'\n")

    def concat_videos(self, txt_file="files.txt", output_file="input_video.mp4"):
        txt_path = f"{self.temp_dir}/{txt_file}"
        video_path = f"{self.temp_dir}/{output_file}"
    
        ffmpeg_command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", txt_path, "-c", "copy", video_path, "-y"]
        subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    def generate_input_video(self, video_duration_sec = 35):
        print('Generating input video')

        # Assuming each video is 5 seconds long
        video_count = math.ceil(video_duration_sec / 5)
        urls = self.select_random_videos(video_count)
        downloaded_files = self.download_videos(urls)
        self.generate_file_list(downloaded_files)
        self.concat_videos()
        print("Input video generation completed!")

    def generate_output_video(self, video_path, audio_path, srt_path, output_path, font_name):
        print('Generating output video. Running ffmpeg command!')
        
        ffmpeg_command = [
            'ffmpeg',
            '-i', video_path, '-i', audio_path,
            # '-i', bg_music_path, # Inputs
            # '-filter_complex', 
            # f"[2]volume=0.8[aud];[1][aud]amix=inputs=2:duration=shortest:dropout_transition=0",
            '-vf', f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles={srt_path}:force_style='Alignment=10,MarginV=0,FontSize=18,PrimaryColour=&H00FFFF,OutlineColour=&H000000,Outline=3,FontName={font_name}:fontsdir=./fonts',tpad=stop_duration=1",
            '-c:a', 'copy',
            '-shortest', output_path, '-y'
            ]
        
        print("Command: ", ' '.join(ffmpeg_command))

        try:
            subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
            print("Output video generation completed!")
        except subprocess.CalledProcessError as e:
            print(f"Error during video concatenation: {e}")