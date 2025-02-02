import json
import os
from scripts.content import ContentManager
from scripts.platform import PlatformManager
from scripts.analytics import AnalyticsManager
from scripts.automation import AutomationManager
from scripts.logging import Logger

def main_menu():
    """Main command-line menu."""
    logger = Logger()
    
    while True:
        print("\n📱 Social Media Manager")
        print("1️⃣  Content Management")
        print("2️⃣  Platform Management")
        print("3️⃣  Engagement & Analytics")
        print("4️⃣  Automation & Scheduling")
        print("5️⃣  Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            ContentManager().menu()
        elif choice == "2":
            PlatformManager().menu()
        elif choice == "3":
            AnalyticsManager().menu()
        elif choice == "4":
            AutomationManager().menu()
        elif choice == "5":
            print("\n👋 Exiting...")
            logger.log("Program exited successfully.")
            break
        else:
            print("❌ Invalid choice, try again.")

