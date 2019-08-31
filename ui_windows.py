import curses

from ui_utils import UIUtils

class UIWindows(object):
    class BaseWindow(object):
        """Base class for windows."""
        def clear_window(self):
            self.win.erase()

        def refresh_window(self):
            self.win.refresh()

        def get_input(self):
            return self.win.getch()
        
        def add_string(self, string):
            self.win.addstr(string)
            self.refresh_window()
        
        def add_char(self, char, y, x):
            self.win.addstr(0, 0, char)
            self.refresh_window()

        def delete_char(self, y, x):
            self.win.delch(y, x)
            self.refresh_window()

        def change_text(self, new_text):
            self.clear_window()
            self.add_string(new_text)
            self.refresh_window()

    class TopBar(BaseWindow):
        def __init__(self):
            self.win = UIUtils.make_window("top_bar")
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
            self.win = UIUtils.make_window("bottom_bar")
            self.is_user_input = False
            self.is_pagination_active = False
            self.pagination_pages = []
            self.current_command = ""
        
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
            self.win = UIUtils.make_window("chat_body")
            self.chat_log = []
            self.displayed_chat_log = []
        
        def set_chat_log(self, chat_log):
            self.chat_log = chat_log
            self.displayed_chat_log = chat_log[0:curses.LINES - 3]
            count = self.win.getmaxyx()[0] - 1
            for i in self.displayed_chat_log:
                self.add_char(0, 0, f"({i[0]}) {i[1]}: {i[2]}")
