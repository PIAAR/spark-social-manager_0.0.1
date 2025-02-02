import json
import datetime

class Logger:
    LOG_FILE = "data/logs.json"

    def log(self, message):
        """Logs messages with timestamp."""
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {"timestamp": timestamp, "message": message}

        logs = self.load_logs()
        logs.append(log_entry)
        self.save_logs(logs)

    def load_logs(self):
        """Loads logs from JSON file."""
        try:
            with open(self.LOG_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_logs(self, logs):
        """Saves logs to JSON file."""
        with open(self.LOG_FILE, "w") as file:
            json.dump(logs, file, indent=4)

    def view_logs(self):
        """Prints logs to console."""
        logs = self.load_logs()
        print("\n📜 Log History:")
        for entry in logs:
            print(f"{entry['timestamp']} - {entry['message']}")
