import curses

from textwrap import wrap
from ui.ui_windows.base_window import BaseWindow

class ChatBody(BaseWindow):
    def __init__(self):
        super().__init__("chat_body")
        self.chat_log = []
        self.current_y_pos = curses.LINES - 3

    def scroll_chat_log(self, value):
        self.current_y_pos += value
        self.refresh_chat_log()

    def set_chat_log(self, chat_log):
        self.current_y_pos = curses.LINES - 3
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
    
    def create_ansi_map(self, content):
        ansi_mapping = {}
        started_styles = {
                    "italic": False,
                    "bold": False,
                    "underline": False,
                }
        for idx,c in enumerate(content):
            if c == "*":
                if content[idx + 1] == "*":
                    started_styles["bold"] = not started_styles["bold"]
                    ansi_mapping[idx] = -1
                else:
                    started_styles["italic"] = not started_styles["italic"]
                    ansi_mapping[idx] = -1
            elif c == "_" and content[idx + 1] == "_":
                started_styles["underline"] = not started_styles["underline"]
                ansi_mapping[idx] = -1
            else:
                current_style = curses.A_NORMAL
                if started_styles["bold"]:
                    current_style += curses.A_BOLD
                if started_styles["italic"]:
                    current_style += curses.A_ITALIC
                if started_styles["underline"]:
                    current_style += curses.A_UNDERLINE
                ansi_mapping[idx] = current_style
        return ansi_mapping
    
    def refresh_chat_log(self):
        self.win = curses.newpad(len(self.chat_log), curses.COLS - 1)
        y_pos = self.current_y_pos
        for i in self.chat_log:
            information = ""
            if i.edited_at:
                information += "(edited) "
            name = i.author
            if i.author.display_name != str(i.author)[:-5]:
                name = f"{i.author.display_name} ({str(i.author)})"
            final_string = f"[{i.created_at.strftime('%X')}] {name}: {i.content} {information}"
            final_lines = [final_string]
            if len(final_string) > curses.COLS - 1:
                final_lines = wrap(final_string, width=curses.COLS - 1)
            newline_lines = []
            for string in final_lines:
                newline_lines += string.splitlines()
            final_lines = newline_lines
            final_lines.reverse()
            for string in final_lines:
                ansi_mapping = self.create_ansi_map(string)
                self.add_string(string, False, y_pos, 0, ansi_mapping)
                y_pos -= 1
        self.refresh_window()
