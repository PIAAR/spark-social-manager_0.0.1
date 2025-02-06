import curses
import time
from scripts.content import ContentManager
from scripts.platform import PlatformManager
from scripts.analytics import AnalyticsManager
from scripts.automation import AutomationManager
from SPARK.scripts.log_manager import Logger

# Define menu options
menu_options = [
    "1️⃣  Content Management",
    "2️⃣  Platform Management",
    "3️⃣  Engagement & Analytics",
    "4️⃣  Automation & Scheduling",
    "5️⃣  Logs",
    "6️⃣  Exit"
]

def main_menu(stdscr):
    """Display a centered menu and handle user interaction."""
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()      # Clear the screen
    stdscr.refresh()
    logger = Logger()

    # Get screen dimensions
    height, width = stdscr.getmaxyx()

    current_selection = 0
    while True:
        stdscr.clear()

        # Title Header
        title = "📱 Social Media Manager"
        stdscr.addstr(height // 4, (width - len(title)) // 2, title, curses.A_BOLD)

        # Draw menu options centered
        for idx, option in enumerate(menu_options):
            x = (width - len(option)) // 2
            y = (height // 2 - len(menu_options) // 2) + idx

            # Highlight selected option
            if idx == current_selection:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, option)

        stdscr.refresh()

        # Key handling
        key = stdscr.getch()

        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_options) - 1:
            current_selection += 1
        elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
            if current_selection == len(menu_options) - 1:  # Exit option
                if confirm_exit(stdscr):  # Confirm exit
                    stdscr.clear()
                    stdscr.refresh()
                    logger.log("Program exited successfully.")
                    break
                break
            elif current_selection == 4:  # Logs Menu
                Logger().menu(stdscr)
            else:
                handle_selection(stdscr, current_selection)

def confirm_exit(stdscr):
    """Displays a confirmation screen before exiting."""
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()
    confirm_text = "❗ Are you sure you want to exit? (Y/N) ❗"
    stdscr.addstr(height // 2, (width - len(confirm_text)) // 2, confirm_text, curses.A_BOLD)

    while True:
        key = stdscr.getch()
        if key in [ord("y"), ord("Y")]:  # Yes
            return True
        elif key in [ord("n"), ord("N")]:  # No
            return False

def handle_selection(stdscr, selection):
    """Handles user selection from the main menu."""
    stdscr.clear()
    stdscr.refresh()
    logger = Logger()
    
    functions = [
        ContentManager,
        PlatformManager,
        AnalyticsManager,
        AutomationManager
    ]

    manager = functions[selection]()  # Instantiate class
    manager.menu(stdscr)  # Call the menu function

    if selection == 0:
        logger.log("Opened Content Management")
        submenu(stdscr, "Content Management", ContentManager)
    elif selection == 1:
        logger.log("Opened Platform Management")
        submenu(stdscr, "Platform Management", PlatformManager)
    elif selection == 2:
        logger.log("Opened Engagement & Analytics")
        submenu(stdscr, "Engagement & Analytics", AnalyticsManager)
    elif selection == 3:
        logger.log("Opened Automation & Scheduling")
        submenu(stdscr, "Automation & Scheduling", AutomationManager)

def submenu(stdscr, title, manager_class):
    """Displays a submenu for the selected section."""
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()
    stdscr.addstr(height // 4, (width - len(title)) // 2, title, curses.A_BOLD)
    stdscr.addstr(height // 2, (width // 2) - 10, "🔄 Loading...")

    stdscr.refresh()
    time.sleep(1)  # Simulate loading delay

    stdscr.clear()
    stdscr.refresh()

    # Call the respective manager's menu method
    manager = manager_class()
    manager.menu()

    # Show return message
    stdscr.addstr(height // 2, (width // 2) - 10, "↩ Press any key to return...")
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main_menu)
