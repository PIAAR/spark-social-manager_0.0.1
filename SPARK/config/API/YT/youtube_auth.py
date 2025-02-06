import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Define credentials file paths for multiple accounts
CREDENTIALS_FILE = "yt-credentials.json"
TOKEN_FILES = {
    "personal": "yt-token-personal.json",
    "brand": "yt-token-brand.json"
}

# Define API scope for YouTube access
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_youtube(token_file):
    """Authenticate and return a YouTube API service instance for a specific account."""
    creds = None

    # Remove token to force account selection
    if os.path.exists(token_file):
        os.remove(token_file)

    # Start a fresh authentication flow
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE, SCOPES
    )

    # Force user to select an account & brand account if applicable
    creds = flow.run_local_server(port=0, prompt="consent")

    # Save the token for future use
    with open(token_file, "w") as token:
        token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def get_channels(youtube):
    """Retrieve all YouTube channels linked to the authenticated account."""
    response = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    ).execute()
    
    return response.get("items", [])

def get_videos(youtube, channel_id):
    """Fetch latest videos from a given YouTube channel."""
    response = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=10  # Adjust to fetch more videos
    ).execute()
    
    return response.get("items", [])

if __name__ == "__main__":
    # Authenticate separately for both Personal and Brand accounts
    print("🔹 Authenticate for Personal YouTube Account")
    youtube_personal = authenticate_youtube(TOKEN_FILES["personal"])
    personal_channels = get_channels(youtube_personal)
    
    print("\n🔹 Authenticate for Brand YouTube Account")
    youtube_brand = authenticate_youtube(TOKEN_FILES["brand"])
    brand_channels = get_channels(youtube_brand)

    # Fetch & Display Videos for Both Accounts
    all_channels = {"Personal Account": personal_channels, "Brand Account": brand_channels}

    for account_type, channels in all_channels.items():
        print(f"\n📺 {account_type} Channels:\n" + "=" * 40)
        for channel in channels:
            channel_id = channel["id"]
            channel_title = channel["snippet"]["title"]
            print(f"🎬 Fetching videos for: {channel_title}")

            videos = get_videos(youtube_personal if account_type == "Personal Account" else youtube_brand, channel_id)
            for vid in videos:
                video_title = vid["snippet"]["title"]
                video_url = f"https://www.youtube.com/watch?v={vid['id']['videoId']}"
                print(f"📹 {video_title} → {video_url}")
