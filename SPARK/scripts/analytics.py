class AnalyticsManager:
    def menu(self):
        """Engagement & Analytics Menu"""
        while True:
            print("\n📊 Engagement & Analytics")
            print("1️⃣  View Post Performance")
            print("2️⃣  View Follower Growth")
            print("3️⃣  Monitor Mentions & Hashtags")
            print("4️⃣  Competitor Analysis")
            print("5️⃣  Back to Main Menu")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.view_post_performance()
            elif choice == "2":
                self.view_follower_growth()
            elif choice == "3":
                self.monitor_mentions()
            elif choice == "4":
                self.competitor_analysis()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice, try again.")

    def view_post_performance(self):
        """Retrieve post analytics data."""
        print("\n📈 Viewing Post Performance...")

    def view_follower_growth(self):
        """Retrieve follower growth analytics."""
        print("\n📊 Viewing Follower Growth...")

    def monitor_mentions(self):
        """Monitor social media mentions."""
        print("\n🔎 Monitoring Mentions & Hashtags...")

    def competitor_analysis(self):
        """Analyze competitor trends."""
        print("\n📊 Performing Competitor Analysis...")
