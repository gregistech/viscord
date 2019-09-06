import curses

class UIUtils:
    def make_window(win_type):
        """This creates a specific type of 'window'."""
        if win_type == "top_bar":
                top_bar = curses.newwin(1, curses.COLS - 1, 0, 0)
                top_bar.bkgd(" ", curses.color_pair(1))
                top_bar.refresh()
                return top_bar
        elif win_type == "bottom_bar":
            bottom_bar = curses.newwin(1, curses.COLS - 1, curses.LINES - 1, 0)
            bottom_bar.refresh()
            return bottom_bar
        elif win_type == "chat_body":
            chat_body = curses.newpad(1, curses.COLS - 1)
            return chat_body

    def configure_main_window(stdscr):
        """This configures the colors, and other attributes of our main window."""
        stdscr.nodelay(True)
        stdscr.clear()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

