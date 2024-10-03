import os
import random
import requests
import subprocess

video_urls = [
        "http://raw.githubusercontent.com/shovon588/assets/master/1.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/2.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/3.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/4.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/5.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/6.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/7.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/8.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/9.mp4",
    ]

class VideoEngine:
    def __init__(self, asset_dir, temp_dir = 'tmp'):
        self.asset_dir = asset_dir
        self.temp_dir = temp_dir
        self.text_file_path = f"{self.temp_dir}/text.txt"

    def select_random_videos(self):
        files = os.listdir(self.asset_dir)
        return random.sample(files, 7)

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

    def concat_videos(self, txt_file="files.txt", output_file="output_video.mp4"):
        ffmpeg_command = f"ffmpeg -f concat -safe 0 -i {self.temp_dir}/{txt_file} -c copy {self.temp_dir}/{output_file} -y"
        subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    def generate_input_video_temp(self):
        print('Generating input video')
        urls = random.sample(video_urls, 6)
        downloaded_files = self.download_videos(urls)
        print('Downloaded files: ', downloaded_files)
        print('LIST: ', os.listdir(self.temp_dir))
        self.generate_file_list(downloaded_files)
        self.concat_videos()
        print('Video concatenation done!')
        print('List directory: ', os.listdir())
        print('Temp dir: ', os.listdir('tmp'))
    
    def generate_input_video(self):
        videos = self.select_random_videos()
        with open(self.text_file_path, 'w') as f:
            for video in videos:
                absolute_path = os.path.abspath(f"{self.asset_dir}/{video}")
                f.write(f"file '{absolute_path}'\n")

        ffmpeg_command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', self.text_file_path,
            '-c', 'copy',
            f'{self.temp_dir}/input_video.mp4',
            '-y'
        ]

        try:
            subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
            print("Input video generation completed!")
        except subprocess.CalledProcessError as e:
            print(f"Error during video concatenation: {e}")

    def generate_output_video(self, video_path, audio_path, srt_path, output_path, font_name):
        """
        # Current command
        ffmpeg -i video.mp4 -i output.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles=subtitles.srt:force_style='Alignment=10,MarginV=0,FontSize=22,PrimaryColour=&H000000&,OutlineColour=&HFFFFFF,FontName=Jacquarda Bastarda 9:fontsdir=./',tpad=stop_duration=1" -c:a copy -shortest output_video.mp4 -y
        """

        ffmpeg_command = [
            'ffmpeg', 
            '-i', video_path, 
            '-i', audio_path, 
            '-vf', f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles={srt_path}:force_style='Alignment=10,MarginV=0,FontSize=22,PrimaryColour=&H000000&,OutlineColour=&HFFFFFF,FontName={font_name}:fontsdir=./fonts',tpad=stop_duration=1", 
            '-c:a', 'copy', 
            '-shortest', 
            output_path, 
            '-y'
        ]

        try:
            subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
            print("Output video generation completed!")
        except subprocess.CalledProcessError as e:
            print(f"Error during video concatenation: {e}")