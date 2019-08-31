import curses
import sys
import queue

from ui_utils import UIUtils
from ui_windows import UIWindows
from command_interpreter import CommandInterpreter
from threading import Thread

class UIMain(object):
    def __init__(self, loop_queue, ui_queue):
        self.loop_queue, self.ui_queue = loop_queue, ui_queue
        self.commands = {
                "q": ["system", "exit"],
                "send": ["discord_api", "send_message"],
                "guilds": ["discord_api", "get_all_guilds"],
                "guild": ["discord_api", "switch_to_guild"],
                "channels": ["discord_api", "get_all_channels"],
                "channel": ["discord_api", "switch_to_channel"],}
                
    def setup_ui(self, stdscr):
        """This is called by the curses wrapper, it configures the main window, makes the bars and starts the UI loop."""
        UIUtils.configure_main_window(stdscr)
        self.com_interpreter = CommandInterpreter()
        self.top_bar = UIWindows.TopBar()
        self.bottom_bar = UIWindows.BottomBar()
        self.bottom_bar.win.nodelay(True)
        self.chat_body = UIWindows.ChatBody()
        self.ui_loop()
    
    def handle_queue_tasks(self):
        try:
            new_task = self.ui_queue.get(False)
            if new_task[0]:
                obj = getattr(self, new_task[0])
            else:
                obj = self
            func = getattr(obj, new_task[1])
            try:
                func(*new_task[2])
            except IndexError:
                func()
        except queue.Empty:
            return

    def handle_command(self, com):
        if not com[0] in self.commands.keys():
            return
        task_args = self.commands[com[0]]
        try:
            task_args = (*task_args, com[1])
        except IndexError:
            pass
        finally:
            self.loop_queue.put(tuple(task_args))

    def handle_user_input(self):
            c = self.bottom_bar.get_input()
            if c == -1 or c > 255:
                return
            if c == 27:
                    self.bottom_bar.is_user_input = False
                    self.bottom_bar.is_pagination_active = False
                    self.bottom_bar.current_command = ""
            if not self.bottom_bar.is_pagination_active:
                if c == 58 and not self.bottom_bar.is_user_input:
                    self.bottom_bar.clear_window()
                    self.bottom_bar.is_user_input = True
                if self.bottom_bar.is_user_input:
                    if c == 10: 
                        if len(self.bottom_bar.current_command) > 0:
                            com = self.com_interpreter.interpret(self.bottom_bar.current_command)
                            self.handle_command(com)
                            self.bottom_bar.clear_window()
                            self.bottom_bar.current_command = ""
                            self.bottom_bar.is_user_input = False
                        else:
                            self.bottom_bar.is_user_input = False
                    elif c == 127:
                        if self.bottom_bar.delete_last_char():
                            self.bottom_bar.current_command = self.bottom_bar.current_command[0:-1]
                    else:
                        c = chr(c)
                        if self.bottom_bar.add_user_char(c):
                            self.bottom_bar.current_command += c
            else:
                if c == 10:
                    self.bottom_bar.show_next_page()

    def ui_loop(self):
        while True:
            self.handle_user_input()
            self.handle_queue_tasks()
