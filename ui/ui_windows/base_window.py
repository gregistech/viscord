import curses

from ui.ui_utils import UIUtils

class BaseWindow:
    """Base class for windows."""
    def __init__(self, name):
        self.name = name
        self.resize_window()

    def clear_window(self):
        self.win.erase()

    def refresh_window(self):
        if self.name != "chat_body":
            self.win.refresh()
        else:
            self.win.refresh(0, 0, 1, 0, curses.LINES - 2, curses.COLS - 1)

    def get_input(self):
        return self.win.getch()

    def add_string(self, string, refresh = True, y = None, x = None):
        if y != None and x != None:
            x_offset = 0
            for c in string:
                try:
                    self.add_char(c, y, x + x_offset)
                except curses.error:
                    pass
                x_offset += 1
        else:
            self.win.addstr(string)
        if refresh:
            self.refresh_window()

    def add_char(self, char, y, x):
        self.win.addstr(y, x, char)
        self.refresh_window()

    def delete_char(self, y, x):
        self.win.delch(y, x)
        self.refresh_window()

    def change_text(self, new_text):
        self.clear_window()
        self.add_string(new_text)
        self.refresh_window()

    def resize_window(self):
        self.win = UIUtils.make_window(self.name)
