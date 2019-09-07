import curses

from ui.ui_utils import UIUtils

class UIWindows:
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

    class BottomBar(BaseWindow):
        def __init__(self):
            super().__init__("bottom_bar")
            self.is_user_input = False
            self.is_insert_input = False
            self.is_pagination_active = False
            self.pagination_pages = []
            self.current_command = ""
            self.current_message = ""

        def add_user_char(self, c):
            cur_pos = curses.getsyx()
            if cur_pos[1] + 1 != curses.COLS - len(c):
                self.add_string(c)
                self.refresh_window()
                return True
            return False

        def delete_last_char(self):
            cur_pos = curses.getsyx()
            if cur_pos[1] > 0:
                self.delete_char(0, cur_pos[1] - 1)
                self.refresh_window()
                return True
            return False

        def build_option_string_array(self, options):
            builded_array = []
            for i in options:
                builded_array.append(f"|{i}|")
            return builded_array

        def paginate_options(self, options):
            options = list(options)
            builded_text = " ".join(self.build_option_string_array(options)) + " (Page 0/0)"
            if len(builded_text) >= curses.COLS - 15:
                builded_text = ""
                builded_array = []
                pages = []
                while len(options) > 0:
                    while not len(builded_text + f" (Page {len(pages)}/xxxxxx)") >= curses.COLS - 15 and len(options) > 0:
                        try:
                            builded_array.append(options.pop())
                        except IndexError:
                            continue
                        builded_text = " ".join(self.build_option_string_array(builded_array))
                    pages.append(builded_text)
                    builded_array = []
                    builded_text = ""
                count = 0
                for i in pages:
                    pages[count] = i + f" (Page {count}/{len(pages) - 1})"
                    count += 1
                self.pagination_pages = pages[:: -1]
                self.pagination_active = True
                self.show_next_page()
            else:
                self.change_text(builded_text)

        def show_next_page(self):
            if len(self.pagination_pages) > 0:
                self.is_pagination_active = True
                current_page = self.pagination_pages.pop()
                if len(self.pagination_pages) < 0:
                    self.is_pagination_active = False
                self.change_text(current_page)
            else:
                self.is_pagination_active = False
                self.pagination_pages = []
                self.pagination_size = 0

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
                self.add_string(f"[{i.created_at.strftime('%X')}] {i.author}: {i.content} {information}", False, y_pos, 0)
                y_pos -= 1
            self.refresh_window()

