import curses

from ui.ui_windows.base_window import BaseWindow

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
        if cur_pos[1] > 0 and (len(self.current_message) > 0 or len(self.current_command) > 0):
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
