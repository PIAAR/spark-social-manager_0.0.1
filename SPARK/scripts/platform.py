import json

class PlatformManager:
    CREDENTIALS_FILE = "data/credentials.json"

    def menu(self):
        """Platform Management Menu"""
        while True:
            print("\n🔗 Platform Management")
            print("1️⃣  Connect Account")
            print("2️⃣  Disconnect Account")
            print("3️⃣  View Connected Accounts")
            print("4️⃣  Back to Main Menu")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.connect_account()
            elif choice == "2":
                self.disconnect_account()
            elif choice == "3":
                self.view_connected_accounts()
            elif choice == "4":
                break
            else:
                print("❌ Invalid choice, try again.")

    def connect_account(self):
        """Connects an account and stores credentials in JSON."""
        platform = input("\nEnter platform name (Twitter, Facebook, etc.): ")
        api_key = input("Enter API Key: ")
        api_secret = input("Enter API Secret: ")

        credentials = self.load_credentials()
        credentials[platform] = {"api_key": api_key, "api_secret": api_secret}
        self.save_credentials(credentials)

        print(f"✅ {platform} connected successfully.")

    def disconnect_account(self):
        """Disconnects an account."""
        platform = input("\nEnter platform name to disconnect: ")
        credentials = self.load_credentials()

        if platform in credentials:
            del credentials[platform]
            self.save_credentials(credentials)
            print(f"✅ {platform} disconnected successfully.")
        else:
            print(f"❌ {platform} not found.")

    def view_connected_accounts(self):
        """View all connected accounts."""
        credentials = self.load_credentials()
        print("\n🔗 Connected Accounts:")
        for platform in credentials.keys():
            print(f"✅ {platform}")

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
