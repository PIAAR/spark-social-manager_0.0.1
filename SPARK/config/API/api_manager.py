import os
import json
import logging
from scripts.log_manager import logger, LogManager
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import tweepy
import requests

# Define file paths
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "../../data/credentials.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "../../data/logs/logs.json")

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

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
        logger.error("❌ Credentials file not found.")
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
            if creds:
                logger.info("✅ YouTube API authentication successful.")
                return build("youtube", "v3", credentials=creds)
            else:
                logger.error("❌ YouTube API authentication failed.")
                return None
        except Exception as e:
            logger.error(f"❌ Failed to authenticate YouTube: {e}")
            return None

    def get_spotify_client(self):
        """Authenticate and return a Spotify API client."""
        try:
            creds = self.credentials.get("spotify", {})
            if not creds:
                logger.error("❌ Spotify credentials missing.")
                return None

            spotify_client = Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=creds["client_id"],
                    client_secret=creds["client_secret"],
                    redirect_uri=creds["redirect_uri"],
                    scope="user-library-read",
                )
            )
            logger.info("✅ Spotify API authentication successful.")
            return spotify_client
        except Exception as e:
            logger.error(f"❌ Failed to authenticate Spotify: {e}")
            return None

    def get_x_client(self):
        """Authenticate and return an X (Twitter) API client."""
        try:
            creds = self.credentials.get("x", {})
            if not creds:
                logger.error("❌ X (Twitter) credentials missing.")
                return None

            auth = tweepy.OAuth1UserHandler(
                creds["api_key"],
                creds["api_secret"],
                creds["access_token"],
                creds["access_secret"],
            )
            twitter_client = tweepy.API(auth)
            logger.info("✅ X (Twitter) API authentication successful.")
            return twitter_client
        except Exception as e:
            logger.error(f"❌ Failed to authenticate X (Twitter): {e}")
            return None

    def get_meta_client(self):
        """Authenticate and return a Meta API client (Facebook/Instagram)."""
        try:
            creds = self.credentials.get("meta", {})
            if not creds:
                logger.error("❌ Meta (Facebook/Instagram) credentials missing.")
                return None

            meta_client = {
                "access_token": creds["access_token"],
                "page_id": creds["page_id"],
            }
            logger.info("✅ Meta API authentication successful.")
            return meta_client
        except Exception as e:
            logger.error(f"❌ Failed to authenticate Meta (Facebook/Instagram): {e}")
            return None

    def get_tiktok_client(self):
        """Authenticate and return a TikTok API client."""
        try:
            creds = self.credentials.get("tiktok", {})
            if not creds:
                logger.error("❌ TikTok credentials missing.")
                return None

            tiktok_client = {
                "access_token": creds["access_token"],
                "client_key": creds["client_key"],
            }
            logger.info("✅ TikTok API authentication successful.")
            return tiktok_client
        except Exception as e:
            logger.error(f"❌ Failed to authenticate TikTok: {e}")
            return None


# Example Usage:
if __name__ == "__main__":
    manager = APIManager()

    print("\n🔹 Authenticating YouTube...")
    youtube_client = manager.get_youtube_client("../config/API/YT/yt-token-brand.json")
    if youtube_client:
        print("✅ YouTube API Ready!")

    print("\n🔹 Authenticating Spotify...")
    spotify_client = manager.get_spotify_client()
    if spotify_client:
        print("✅ Spotify API Ready!")

    print("\n🔹 Authenticating X (Twitter)...")
    x_client = manager.get_x_client()
    if x_client:
        print("✅ X (Twitter) API Ready!")

    print("\n🔹 Authenticating Meta (Facebook/Instagram)...")
    meta_client = manager.get_meta_client()
    if meta_client:
        print("✅ Meta API Ready!")

    print("\n🔹 Authenticating TikTok...")
    tiktok_client = manager.get_tiktok_client()
    if tiktok_client:
        print("✅ TikTok API Ready!")
