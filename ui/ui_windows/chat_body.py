import curses

from textwrap import wrap
from ui.ui_windows.base_window import BaseWindow

class ChatBody(BaseWindow):
    def __init__(self):
        super().__init__("chat_body")
        self.chat_log = []

    def set_chat_log(self, chat_log):
        if chat_log == None:
            self.chat_log = []
        else:
            self.chat_log = chat_log
        self.refresh_chat_log()

    def edit_chat_log(self, old_id, new_message):
        for i in self.chat_log:
            if i.id == old_id:
                self.chat_log[self.chat_log.index(i)] = new_message
                self.refresh_chat_log()
                return

    def add_to_chat_log(self, message):
        self.chat_log.insert(0, message)
        self.refresh_chat_log()

    def refresh_chat_log(self):
        self.win = curses.newpad(len(self.chat_log), curses.COLS - 1)
        y_pos = curses.LINES - 3
        for i in self.chat_log:
            information = ""
            if i.edited_at:
                information += "(edited) "
            final_string = f"[{i.created_at.strftime('%X')}] {i.author}: {i.content} {information}"
            final_lines = [final_string]
            if len(final_string) > curses.COLS - 1:
                final_lines = wrap(final_string, width=curses.COLS - 1)
            newline_lines = []
            for string in final_lines:
                newline_lines += string.splitlines()
            final_lines = newline_lines
            final_lines.reverse()
            for string in final_lines:
                self.add_string(string, False, y_pos, 0)
                y_pos -= 1
        self.refresh_window()
