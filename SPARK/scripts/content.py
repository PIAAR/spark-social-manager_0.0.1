class ContentManager:
    def menu(self):
        """Content Management Menu"""
        while True:
            print("\n📝 Content Management")
            print("1️⃣  Create Post")
            print("2️⃣  Edit Post")
            print("3️⃣  Delete Post")
            print("4️⃣  Schedule Post")
            print("5️⃣  View Scheduled Posts")
            print("6️⃣  Back to Main Menu")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.create_post()
            elif choice == "2":
                self.edit_post()
            elif choice == "3":
                self.delete_post()
            elif choice == "4":
                self.schedule_post()
            elif choice == "5":
                self.view_scheduled_posts()
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice, try again.")

    def create_post(self):
        """Create a new social media post."""
        print("\n📝 Creating Post...")

    def edit_post(self):
        """Edit an existing post."""
        print("\n✏️ Editing Post...")

    def delete_post(self):
        """Delete a post."""
        print("\n🗑️ Deleting Post...")

    def schedule_post(self):
        """Schedule a post."""
        print("\n📅 Scheduling Post...")

    def view_scheduled_posts(self):
        """View all scheduled posts."""
        print("\n📂 Viewing Scheduled Posts...")
