import curses
from scripts.content import ContentManager
from scripts.platform import PlatformManager
from scripts.analytics import AnalyticsManager
from scripts.automation import AutomationManager
from scripts.logging import Logger

# Define menu options
menu_options = [
    "1️⃣  Content Management",
    "2️⃣  Platform Management",
    "3️⃣  Engagement & Analytics",
    "4️⃣  Automation & Scheduling",
    "5️⃣  Exit"
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
                stdscr.clear()
                stdscr.refresh()
                logger.log("Program exited successfully.")
                break
            handle_selection(stdscr, current_selection)

def handle_selection(stdscr, selection):
    """Handles user selection from the menu."""
    stdscr.clear()
    stdscr.refresh()

    if selection == 0:
        ContentManager().menu()
    elif selection == 1:
        PlatformManager().menu()
    elif selection == 2:
        AnalyticsManager().menu()
    elif selection == 3:
        AutomationManager().menu()

    stdscr.addstr(7, 10, "Press any key to return to the menu...")
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main_menu)
