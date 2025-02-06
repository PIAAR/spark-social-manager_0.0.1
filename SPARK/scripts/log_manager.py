import logging
import curses
import json
import os
import datetime

LOG_FILES = {
    "General Logs": "data/logs.json",
    "Automation Logs": "data/automation_logs.json"
}

# Set up centralized logging using Python's built-in logging module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)  # This can be used in other modules

class LogManager:
    """Handles logging operations and UI-based log management."""

    DEFAULT_LOG_FILE = LOG_FILES["General Logs"]

    def __init__(self):
        """Initializes LogManager and ensures log directories exist."""
        os.makedirs(os.path.dirname(self.DEFAULT_LOG_FILE), exist_ok=True)

    def log(self, message, log_file=DEFAULT_LOG_FILE):
        """
        Logs a message with a timestamp.

        Args:
            message (str): The log message.
            log_file (str, optional): The log file path.
        """
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {"timestamp": timestamp, "message": message}

        logs = self.load_logs(log_file)
        logs.append(log_entry)
        self.save_logs(log_file, logs)

    def load_logs(self, log_file):
        """
        Loads logs from the specified JSON file.

        Args:
            log_file (str): The log file path.

        Returns:
            list: A list of log entries.
        """
        if not os.path.exists(log_file):
            return []

        try:
            with open(log_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_logs(self, log_file, logs):
        """
        Saves logs to a JSON file.

        Args:
            log_file (str): The log file path.
            logs (list): A list of log entries.
        """
        try:
            with open(log_file, "w") as file:
                json.dump(logs, file, indent=4)
        except Exception as e:
            logging.error(f"❌ Error saving logs: {e}")
            print(f"❌ Error saving logs: {e}")

    def clear_logs(self, log_file):
        """
        Clears all logs in the specified log file.

        Args:
            log_file (str): The log file path.
        """
        self.save_logs(log_file, [])
        logging.info(f"✅ Logs cleared for {log_file}")
        print(f"✅ Logs cleared for {log_file}")

    def view_logs(self, log_file):
        """
        Displays logs from a specified file.

        Args:
            log_file (str): The log file path.
        """
        logs = self.load_logs(log_file)
        print("\n📜 Log History:")
        if not logs:
            print("❌ No logs available.")
        for entry in logs:
            print(f"{entry['timestamp']} - {entry['message']}")

    # ---------- Curses UI Section ----------

    def menu(self, stdscr):
        """Displays the Logs Menu inside curses."""
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        height, width = stdscr.getmaxyx()

        log_options = [
            "1️⃣  View Logs",
            "2️⃣  Clear Logs",
            "3️⃣  Back to Main Menu"
        ]

        current_selection = 0
        while True:
            stdscr.clear()
            title = "📜 Log Management"
            stdscr.addstr(height // 4, (width - len(title)) // 2, title, curses.A_BOLD)

            for idx, option in enumerate(log_options):
                x = (width - len(option)) // 2
                y = (height // 2 - len(log_options) // 2) + idx

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
            elif key == curses.KEY_DOWN and current_selection < len(log_options) - 1:
                current_selection += 1
            elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
                if current_selection == len(log_options) - 1:  # Back to Main Menu
                    break
                elif current_selection == 0:
                    self.view_logs_ui(stdscr)
                elif current_selection == 1:
                    self.clear_logs_ui(stdscr)

    def view_logs_ui(self, stdscr):
        """Displays log entries inside the terminal UI."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(height // 4, (width - 10) // 2, "📜 Select Log File")
        log_names = list(LOG_FILES.keys())

        current_selection = 0
        while True:
            stdscr.clear()
            stdscr.addstr(height // 4, (width - 10) // 2, "📜 Select Log File")

            for idx, log_name in enumerate(log_names):
                x = (width - len(log_name)) // 2
                y = (height // 2 - len(log_names) // 2) + idx

                if idx == current_selection:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, log_name)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, log_name)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP and current_selection > 0:
                current_selection -= 1
            elif key == curses.KEY_DOWN and current_selection < len(log_names) - 1:
                current_selection += 1
            elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
                self.display_log_entries(stdscr, LOG_FILES[log_names[current_selection]])
                break

    def display_log_entries(self, stdscr, log_file):
        """Displays log entries from the selected log file."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        logs = self.load_logs(log_file)

        if logs:
            y = height // 4
            for entry in logs[-10:]:  # Show last 10 logs
                log_text = f"{entry['timestamp']} - {entry['message']}"
                stdscr.addstr(y, 2, log_text[:width - 4])
                y += 1
        else:
            stdscr.addstr(height // 2, (width // 2) - 10, "❌ No logs found.")

        stdscr.refresh()
        stdscr.addstr(height - 2, 2, "↩ Press any key to return...")
        stdscr.getch()

    def clear_logs_ui(self, stdscr):
        """Clears logs from a selected log file."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height // 4, (width // 2) - 10, "⚠️ Select Log File to Clear")

        log_names = list(LOG_FILES.keys())

        current_selection = 0
        while True:
            stdscr.clear()
            stdscr.addstr(height // 4, (width // 2) - 10, "⚠️ Select Log File to Clear")

            for idx, log_name in enumerate(log_names):
                y = (height // 2 - len(log_names) // 2) + idx

                if idx == current_selection:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, 2, log_name)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 2, log_name)

            stdscr.refresh()
            key = stdscr.getch()

            if key in [curses.KEY_ENTER, 10, 13]:
                self.clear_logs(LOG_FILES[log_names[current_selection]])
                stdscr.addstr(height - 2, 2, "✅ Logs Cleared! ↩ Press any key to return...")
                stdscr.getch()
                break

# Example of logging directly in LogManager
logger.info("LogManager initialized successfully.")
