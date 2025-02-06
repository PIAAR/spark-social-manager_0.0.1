import curses
import json
import os
import subprocess
import time

from config.API.api_manager import APIManager
from SPARK.scripts.log_manager import Logger

# Define file paths
CREDENTIALS_FILE = "data/credentials.json"

"""Purpose for Platform Manager

This module handles the platform API management operations, such as connecting and disconnecting accounts, refreshing/updating token data in JSON files for each account, viewing connected accounts, and navigating the platform management menu.
"""

class PlatformManager:
    """Handles Platform Management Operations."""

    def __init__(self):
        self.logger = Logger()
        self.api_manager = APIManager()

    def menu(self, stdscr):
        """Display Platform Management Menu using curses."""
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        height, width = stdscr.getmaxyx()

        platform_options = [
            "1️⃣  Connect Account",
            "2️⃣  Disconnect Account",
            "3️⃣  View Connected Accounts",
            "4️⃣  API Manager (Authentication Control)",
            "5️⃣  Edit API Configuration",
            "6️⃣  Back to Main Menu"
        ]

        current_selection = 0

        while True:
            stdscr.clear()
            title = "🔗 Platform Management"
            stdscr.addstr(height // 4, (width - len(title)) // 2, title, curses.A_BOLD)

            for idx, option in enumerate(platform_options):
                x = (width - len(option)) // 2
                y = (height // 2 - len(platform_options) // 2) + idx

                if idx == current_selection:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, option)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, option)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP and current_selection > 0:
                current_selection -= 1
            elif key == curses.KEY_DOWN and current_selection < len(platform_options) - 1:
                current_selection += 1
            elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
                if current_selection == len(platform_options) - 1:  # Back to Main Menu
                    break
                elif current_selection == 0:
                    self.connect_account(stdscr)
                elif current_selection == 1:
                    self.disconnect_account(stdscr)
                elif current_selection == 2:
                    self.view_connected_accounts(stdscr)
                elif current_selection == 3:
                    self.api_auth_menu(stdscr)
                elif current_selection == 4:
                    self.edit_api_configuration(stdscr)
                else:
                    self.handle_selection(stdscr, current_selection)

    def handle_selection(self, stdscr, selection):
        """Handles user selection and executes corresponding function."""
        stdscr.clear()
        stdscr.refresh()

        functions = [
            self.connect_account,
            self.disconnect_account,
            self.view_connected_accounts
        ]

        action_text = f"🔄 Executing: {functions[selection].__name__.replace('_', ' ').title()}..."
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height // 2, (width - len(action_text)) // 2, action_text, curses.A_BOLD)
        stdscr.refresh()
        time.sleep(1.5)  # Simulate loading delay

        # Call the selected function
        functions[selection](stdscr)

        # Wait for user input before returning to the menu
        stdscr.addstr(height // 2 + 2, (width // 2) - 10, "↩ Press any key to return...")
        stdscr.getch()

    def connect_account(self, stdscr):
        """Connects an account and stores credentials in JSON."""
        stdscr.clear()
        stdscr.refresh()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(height // 4, (width // 2) - 10, "🔗 Connecting Account...")
        stdscr.refresh()
        time.sleep(1)

        platform = self.input_prompt(stdscr, "Enter platform name (Twitter, Facebook, etc.): ")
        api_key = self.input_prompt(stdscr, "Enter API Key: ")
        api_secret = self.input_prompt(stdscr, "Enter API Secret: ")

        credentials = self.load_credentials()
        credentials[platform] = {"api_key": api_key, "api_secret": api_secret}
        self.save_credentials(credentials)

        success_msg = f"✅ {platform} connected successfully."
        stdscr.addstr(height // 2, (width - len(success_msg)) // 2, success_msg, curses.A_BOLD)
        stdscr.refresh()
        time.sleep(2)

    def disconnect_account(self, stdscr):
        """Disconnects an account."""
        stdscr.clear()
        stdscr.refresh()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(height // 4, (width // 2) - 10, "🔗 Disconnecting Account...")
        stdscr.refresh()
        time.sleep(1)

        platform = self.input_prompt(stdscr, "Enter platform name to disconnect: ")
        credentials = self.load_credentials()

        if platform in credentials:
            del credentials[platform]
            self.save_credentials(credentials)
            success_msg = f"✅ {platform} disconnected successfully."
        else:
            success_msg = f"❌ {platform} not found."

        stdscr.addstr(height // 2, (width - len(success_msg)) // 2, success_msg, curses.A_BOLD)
        stdscr.refresh()
        time.sleep(2)
        
    def view_connected_accounts(self, stdscr):
        """View all connected accounts."""
        stdscr.clear()
        stdscr.refresh()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(height // 4, (width // 2) - 10, "🔗 Connected Accounts:")
        credentials = self.api_manager.load_credentials()
        
        for y, platform in enumerate(credentials.keys(), start=7):
            stdscr.addstr(y, 7, f"✅ {platform}")
            
        if not credentials:
            stdscr.addstr(height // 2, (width // 2) - 10, "❌ No connected accounts.", curses.A_BOLD)
        else:
            y_offset = height // 2
            for idx, platform in enumerate(credentials.keys()):
                stdscr.addstr(y_offset + idx, (width // 2) - 10, f"✅ {platform}")

        stdscr.refresh()
        stdscr.addstr(y + 2, 5, "↩ Press any key to return...")
        stdscr.getch()
        time.sleep(3)

    def input_prompt(self, stdscr, prompt):
        """Display a prompt and get user input."""
        curses.echo()  # Enable text input visibility
        stdscr.addstr(curses.LINES - 2, 2, prompt, curses.A_BOLD)
        stdscr.refresh()
        input_value = stdscr.getstr(curses.LINES - 2, len(prompt) + 2, 50).decode("utf-8")
        curses.noecho()  # Disable text input visibility
        return input_value.strip()

    def load_credentials(self):
        """Loads credentials from JSON file."""
        try:
            with open(self.CREDENTIALS_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_credentials(self, credentials):
        """Saves credentials to JSON file."""
        with open(self.CREDENTIALS_FILE, "w") as file:
            json.dump(credentials, file, indent=4)
            
    def api_auth_menu(self, stdscr):
        """Handles API authentication for different platforms."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        api_options = [
            "1️⃣  Authenticate YouTube",
            "2️⃣  Authenticate Spotify",
            "3️⃣  Authenticate X (Twitter)",
            "4️⃣  Authenticate Meta (Facebook/Instagram)",
            "5️⃣  Authenticate TikTok",
            "6️⃣  Back to Platform Menu"
        ]

        current_selection = 0
        while True:
            stdscr.clear()
            title = "🔑 API Authentication"
            stdscr.addstr(height // 4, (width - len(title)) // 2, title, curses.A_BOLD)

            for idx, option in enumerate(api_options):
                x = (width - len(option)) // 2
                y = (height // 2 - len(api_options) // 2) + idx

                if idx == current_selection:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, option)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, option)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP and current_selection > 0:
                current_selection -= 1
            elif key == curses.KEY_DOWN and current_selection < len(api_options) - 1:
                current_selection += 1
            elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
                if current_selection == len(api_options) - 1:  # Back to Platform Menu
                    break
                elif current_selection == 0:
                    self.authenticate_youtube(stdscr)
                elif current_selection == 1:
                    self.authenticate_spotify(stdscr)
                elif current_selection == 2:
                    self.authenticate_x(stdscr)
                elif current_selection == 3:
                    self.authenticate_meta(stdscr)
                elif current_selection == 4:
                    self.authenticate_tiktok(stdscr)

    def authenticate_youtube(self, stdscr):
        """Authenticates YouTube API."""
        stdscr.clear()
        stdscr.addstr(5, 5, "🔹 Authenticating YouTube...")
        self.api_manager.get_youtube_client("config/API/YT/yt-token-brand.json")
        stdscr.addstr(7, 5, "✅ YouTube API Ready!")
        stdscr.refresh()
        stdscr.getch()

    def authenticate_spotify(self, stdscr):
        """Authenticates Spotify API."""
        stdscr.clear()
        stdscr.addstr(5, 5, "🔹 Authenticating Spotify...")
        self.api_manager.get_spotify_client()
        stdscr.addstr(7, 5, "✅ Spotify API Ready!")
        stdscr.refresh()
        stdscr.getch()

    def authenticate_x(self, stdscr):
        """Authenticates X (Twitter) API."""
        stdscr.clear()
        stdscr.addstr(5, 5, "🔹 Authenticating X (Twitter)...")
        self.api_manager.get_x_client()
        stdscr.addstr(7, 5, "✅ X (Twitter) API Ready!")
        stdscr.refresh()
        stdscr.getch()

    def authenticate_meta(self, stdscr):
        """Authenticates Meta (Facebook/Instagram) API."""
        stdscr.clear()
        stdscr.addstr(5, 5, "🔹 Authenticating Meta...")
        self.api_manager.get_meta_client()
        stdscr.addstr(7, 5, "✅ Meta API Ready!")
        stdscr.refresh()
        stdscr.getch()

    def authenticate_tiktok(self, stdscr):
        """Authenticates TikTok API."""
        stdscr.clear()
        stdscr.addstr(5, 5, "🔹 Authenticating TikTok...")
        self.api_manager.get_tiktok_client()
        stdscr.addstr(7, 5, "✅ TikTok API Ready!")
        stdscr.refresh()
        stdscr.getch()

    def edit_api_configuration(self, stdscr):
        """Allows editing of API credentials using a text editor."""
        stdscr.clear()
        stdscr.addstr(5, 5, f"📝 Opening {CREDENTIALS_FILE} in editor...")
        stdscr.refresh()
        subprocess.run(["nano", CREDENTIALS_FILE])  # Change "nano" to "vim" if preferred
        stdscr.addstr(7, 5, "✅ Changes saved! Returning to menu...")
        stdscr.refresh()
        stdscr.getch()