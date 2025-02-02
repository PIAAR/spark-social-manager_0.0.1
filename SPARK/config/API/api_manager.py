import os
import json
import logging
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import tweepy
import requests

# Define file paths
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "../data/credentials.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "../data/logs.json")

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class APIManager:
    """Centralized API Manager for handling authentication and connections."""

    def __init__(self):
        """Load credentials from the JSON file."""
        self.credentials = self.load_credentials()

    def load_credentials(self):
        """Load API credentials from JSON."""
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as file:
                return json.load(file)
        logging.error("Credentials file not found.")
        return {}

    def get_youtube_client(self, token_file):
        """Authenticate and return a YouTube API client."""
        try:
            creds = None
            if os.path.exists(token_file):
                with open(token_file, "r") as token:
                    creds_data = json.load(token)
                    creds = Credentials.from_authorized_user_info(
                        creds_data,
                        ["https://www.googleapis.com/auth/youtube.force-ssl"],
                    )
            return build("youtube", "v3", credentials=creds)
        except Exception as e:
            logging.error(f"Failed to authenticate YouTube: {e}")
            return None

    def get_spotify_client(self):
        """Authenticate and return a Spotify API client."""
        try:
            creds = self.credentials.get("spotify", {})
            return Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=creds["client_id"],
                    client_secret=creds["client_secret"],
                    redirect_uri=creds["redirect_uri"],
                    scope="user-library-read",
                )
            )
        except Exception as e:
            logging.error(f"Failed to authenticate Spotify: {e}")
            return None

    def get_x_client(self):
        """Authenticate and return an X (Twitter) API client."""
        try:
            creds = self.credentials.get("x", {})
            auth = tweepy.OAuth1UserHandler(
                creds["api_key"],
                creds["api_secret"],
                creds["access_token"],
                creds["access_secret"],
            )
            return tweepy.API(auth)
        except Exception as e:
            logging.error(f"Failed to authenticate X (Twitter): {e}")
            return None

    def get_meta_client(self):
        """Authenticate and return a Meta API client (Facebook/Instagram)."""
        try:
            creds = self.credentials.get("meta", {})
            return {"access_token": creds["access_token"], "page_id": creds["page_id"]}
        except Exception as e:
            logging.error(f"Failed to authenticate Meta (Facebook/Instagram): {e}")
            return None

    def get_tiktok_client(self):
        """Authenticate and return a TikTok API client."""
        try:
            creds = self.credentials.get("tiktok", {})
            return {
                "access_token": creds["access_token"],
                "client_key": creds["client_key"],
            }
        except Exception as e:
            logging.error(f"Failed to authenticate TikTok: {e}")
            return None


# Example Usage:
if __name__ == "__main__":
    manager = APIManager()

    print("\n🔹 Authenticating YouTube...")
    if youtube := manager.get_youtube_client(
        "../config/API/YT/yt-token-brand.json"
    ):
        print("✅ YouTube API Ready!")

    print("\n🔹 Authenticating Spotify...")
    if spotify := manager.get_spotify_client():
        print("✅ Spotify API Ready!")

    print("\n🔹 Authenticating X (Twitter)...")
    if x := manager.get_x_client():
        print("✅ X (Twitter) API Ready!")

    print("\n🔹 Authenticating Meta (Facebook/Instagram)...")
    if meta := manager.get_meta_client():
        print("✅ Meta API Ready!")

    print("\n🔹 Authenticating TikTok...")
    if tiktok := manager.get_tiktok_client():
        print("✅ TikTok API Ready!")
