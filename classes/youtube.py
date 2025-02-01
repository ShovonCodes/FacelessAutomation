import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

class YoutubeEngine:
    def __init__(self, video_file_path, refresh_token_key, tags = None, description = None):
        self.video_file_path = video_file_path
        self.refresh_token_key = refresh_token_key
        self.tags = tags if tags else []
        self.description = description if description else ""

    def upload_video(self, title,):
        print('The refresh token key: ', self.refresh_token_key)
        client_id = os.getenv('YOUTUBE_CLIENT_ID')
        client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
        refresh_token = os.getenv(self.refresh_token_key)

        print('Reporting from upload_video')

        if client_id: print('Client ID found')
        if client_secret: print('Client Secret found')
        if refresh_token: print('Refresh Token found')

        credentials = Credentials(
            token=None,  # No need to provide this; it will be refreshed automatically
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri="https://oauth2.googleapis.com/token"
        )
        youtube = build('youtube', 'v3', credentials=credentials)

        media = MediaFileUpload(self.video_file_path, chunksize=-1, resumable=True)

        # Prepare the request body
        request_body = {
            'snippet': {
                'title': title,
                'description': self.description,
                'tags': self.tags,
                'categoryId': '24' # Entertainment
            },
            'status': {
                'privacyStatus': 'public',
                'madeForKids': False,
                'selfDeclaredMadeForKids': False
                }
        }

        # Call the API to upload the video
        request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")

        print("Upload complete! Video URL: https://www.youtube.com/watch?v=" + response['id'])
