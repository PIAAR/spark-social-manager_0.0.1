import curses
import json
import os
import time
from datetime import datetime
from scripts.log_manager import LogManager  # Centralized logging

# Define JSON files for scheduling and logging
AUTOMATION_FILE = "data/scheduled_automations.json"
AUTOMATION_LOGS = "data/logs/automation_logs.json"

class AutomationManager:
    """Handles Automation & Scheduling Operations"""
    
    def __init__(self):
        """Initializes the automation manager and logging."""
        self.logger = LogManager()  # ✅ Fix: Remove log_file parameter

    def menu(self, stdscr):
        """Display Automation & Scheduling Menu using curses."""
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        height, width = stdscr.getmaxyx()

        automation_options = [
            "1️⃣  Create Automated Posting Rules",
            "2️⃣  Hashtag Suggestions",
            "3️⃣  AI Caption & Image Suggestions",
            "4️⃣  Batch Upload Content",
            "5️⃣  Cross-Post to Multiple Platforms",
            "6️⃣  View & Manage Scheduled Posts",
            "7️⃣  Back to Main Menu"
        ]

        current_selection = 0

        while True:
            stdscr.clear()
            title = "🤖 Automation & Scheduling"
            stdscr.addstr(height // 4, (width - len(title)) // 2, title, curses.A_BOLD)

            for idx, option in enumerate(automation_options):
                x = (width - len(option)) // 2
                y = (height // 2 - len(automation_options) // 2) + idx

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
            elif key == curses.KEY_DOWN and current_selection < len(automation_options) - 1:
                current_selection += 1
            elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
                if current_selection == len(automation_options) - 1:  # Back to Main Menu
                    break
                else:
                    self.handle_selection(stdscr, current_selection)

    def handle_selection(self, stdscr, selection):
        """Handles user selection and executes corresponding function."""
        stdscr.clear()
        stdscr.refresh()

        functions = [
            self.create_automation_rules,
            self.hashtag_suggestions,
            self.ai_caption_suggestions,
            self.batch_upload,
            self.cross_post,
            self.view_scheduled_posts
        ]

        action_text = f"🔄 Executing: {functions[selection].__name__.replace('_', ' ').title()}..."
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height // 2, (width - len(action_text)) // 2, action_text, curses.A_BOLD)
        stdscr.refresh()
        time.sleep(1.5)  # Simulate loading delay

        functions[selection](stdscr)

        stdscr.addstr(height // 2 + 2, (width // 2) - 10, "↩ Press any key to return...")
        stdscr.getch()

    def view_scheduled_posts(self, stdscr):
        """Displays scheduled posts and allows deleting or rescheduling them."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height // 4, (width // 2) - 10, "📅 Scheduled Posts")

        scheduled_data = self.load_scheduled_automations()
        posts = scheduled_data.get("scheduled_posts", [])

        if not posts:
            stdscr.addstr(height // 2, (width // 2) - 10, "❌ No scheduled posts.", curses.A_BOLD)
            self.logger.log("No scheduled posts found.")
            stdscr.refresh()
            time.sleep(2)
            return  # ✅ Fix: Ensure function exits here

    def reschedule_post(self, posts, index, scheduled_data):
        """Allows user to reschedule a post."""
        post = posts[index]
        new_time = input(f"\n⏳ Enter new scheduled time for {post['post_text']} (YYYY-MM-DD HH:MM:SS): ")

        try:
            datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")  # Validate format
            posts[index]["scheduled_time"] = new_time
            self.save_scheduled_automations(scheduled_data)
            self.logger.log(f"Rescheduled post: {post} to {new_time}")  # ✅ Fix: Log after saving
            print(f"✅ Post rescheduled for {new_time}")  # ✅ Fix: Print after saving
        except ValueError:
            print("❌ Invalid date format. Try again.")

    def load_scheduled_automations(self):
        """Loads scheduled automations from JSON file, handling errors gracefully."""
        if not os.path.exists(AUTOMATION_FILE):
            return {}

        try:
            with open(AUTOMATION_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            self.logger.log("Error loading scheduled automations JSON.")
            return {}

    def save_scheduled_automations(self, scheduled_data):
        """Saves automation rules to JSON file with error handling."""
        try:
            with open(AUTOMATION_FILE, "w") as file:
                json.dump(scheduled_data, file, indent=4)
            self.logger.log("Scheduled automations saved successfully.")
        except Exception as e:
            self.logger.log(f"Error saving scheduled automations: {e}")

    def check_and_execute_scheduled_posts(self):
        """Checks scheduled posts and executes if the time has passed."""
        scheduled_data = self.load_scheduled_automations()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        remaining_posts = []
        for post in scheduled_data.get("scheduled_posts", []):
            if post["scheduled_time"] <= now:
                self.logger.log(f"Executing scheduled post: {post}")
                print(f"🚀 Posting now on {post['platform']}: {post['post_text']}")
                # Here, integrate API calls to post it
            else:
                remaining_posts.append(post)

        scheduled_data["scheduled_posts"] = remaining_posts
        self.save_scheduled_automations(scheduled_data)
