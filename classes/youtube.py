import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

client_id = os.getenv('YOUTUBE_CLIENT_ID')
client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')

credentials = Credentials(
    token=None,  # No need to provide this; it will be refreshed automatically
    refresh_token=refresh_token,
    client_id=client_id,
    client_secret=client_secret,
    token_uri="https://oauth2.googleapis.com/token"
)

youtube = build('youtube', 'v3', credentials=credentials)

tags = [
    "cryptocurrency",
    "Bitcoin",
    "Ethereum",
    "blockchain",
    "NFTs",
    "DeFi",
    "crypto explained",
    "beginner crypto guide",
    "digital currency",
    "meme coins",
    "Dogecoin",
    "altcoins",
    "crypto mining",
    "volatility in crypto",
    "crypto trends",
    "how cryptocurrency works",
    "smart contracts",
    "crypto investing tips",
    "crypto education",
    "Byte Size Crypto",
]

description = "#cryptocurrency #Bitcoin #Ethereum #blockchain #NFTs #cryptoexplained #cryptobasics #cryptoeducation #learncrypto #ByteSizeCrypto"

class YoutubeEngine:
    def __init__(self, video_file_path):
        self.video_file_path = video_file_path
        
        
    def upload_video(self, title,):
        media = MediaFileUpload(self.video_file_path, chunksize=-1, resumable=True)

        # Prepare the request body
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
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
