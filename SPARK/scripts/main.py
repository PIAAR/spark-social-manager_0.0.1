import curses
from scripts.menu import main_menu

if __name__ == "__main__":
    curses.wrapper(main_menu)
