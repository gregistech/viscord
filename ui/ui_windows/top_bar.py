import curses

from ui.ui_windows.base_window import BaseWindow

class TopBar(BaseWindow):
    def __init__(self):
        super().__init__("top_bar")
        self.guild = self.channel = self.topic = ""
        self.change_text("Welcome to Viscord! Use :help to get help!")

    def set_property(self, property_, value):
        if property_ == "all":
            self.guild, self.channel, self.topic = value[0], value[1], value[2]
        else:
            setattr(self, property_, value)
        self.change_text(f"{self.guild} - {self.channel} - {self.topic}")
