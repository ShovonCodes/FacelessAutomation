import os
import random
import requests
import subprocess

def generate_video_url(video_number):
    return f"http://raw.githubusercontent.com/shovon588/assets/master/{video_number}.mp4",

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
        "http://raw.githubusercontent.com/shovon588/assets/master/10.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/11.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/12.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/13.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/14.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/15.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/16.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/17.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/18.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/19.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/20.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/21.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/22.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/23.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/24.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/25.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/26.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/27.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/28.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/29.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/30.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/31.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/32.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/33.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/34.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/35.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/36.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/37.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/38.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/39.mp4",
        "http://raw.githubusercontent.com/shovon588/assets/master/40.mp4",
    ]

class VideoEngine:
    def __init__(self, temp_dir = 'tmp'):
        self.temp_dir = temp_dir

    def select_random_videos(self, count):
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

    def generate_input_video(self):
        print('Generating input video')
        urls = self.select_random_videos(7)
        downloaded_files = self.download_videos(urls)
        self.generate_file_list(downloaded_files)
        self.concat_videos()
        print("Input video generation completed!")

    def generate_output_video(self, video_path, audio_path, srt_path, output_path, font_name):
        print('Generating output video. Running ffmpeg command!')
        """
        # Current command
        ffmpeg -i video.mp4 -i output.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles=subtitles.srt:force_style='Alignment=10,MarginV=0,FontSize=22,PrimaryColour=&H000000&,OutlineColour=&HFFFFFF,FontName=Jacquarda Bastarda 9:fontsdir=./',tpad=stop_duration=1" -c:a copy -shortest output_video.mp4 -y
        """

        # Previous one, without background music
        ffmpeg_command = [
            'ffmpeg', 
            '-i', video_path, 
            '-i', audio_path,
            '-vf', f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles={srt_path}:force_style='Alignment=10,MarginV=0,FontSize=20,PrimaryColour=&H000000&,OutlineColour=&HFFFFFF,FontName={font_name}:fontsdir=./fonts',tpad=stop_duration=1", 
            '-c:a', 'copy', 
            '-shortest', 
            output_path, 
            '-y'
        ]
        
        # ffmpeg_command = [
        #     'ffmpeg',
        #     '-i', video_path, '-i', audio_path,
        #     # '-i', bg_music_path, # Inputs
        #     '-filter_complex', 
        #     f"[2]volume=0.8[aud];[1][aud]amix=inputs=2:duration=shortest:dropout_transition=0",
        #     '-vf', f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles={srt_path}:force_style='Alignment=10,MarginV=0,FontSize=22,PrimaryColour=&H000000&,OutlineColour=&HFFFFFF,FontName={font_name}:fontsdir=./fonts',tpad=stop_duration=1",
        #     '-c:a', 'aac',  # Ensure proper audio codec
        #     '-shortest', output_path, '-y'
        # ]

        try:
            subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
            print("Output video generation completed!")
        except subprocess.CalledProcessError as e:
            print(f"Error during video concatenation: {e}")