import curses

from ui.ui_windows.base_window import BaseWindow

class TopBar(BaseWindow):
    def __init__(self):
        super().__init__("top_bar")
        self.change_text("Welcome to Viscord! Use :help to get help!")

    def set_info(self, guild = "", channel = "", topic = ""):
        text = ""
        if guild != "":
            text += guild
        if channel != "":
            text += f" - #{channel}"
        if topic != "":
            text += f" - {topic}"
        self.change_text(text)
