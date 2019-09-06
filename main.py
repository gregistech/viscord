import discord
import os
import queue
import inspect
import asyncio

from threading import Thread
from curses import wrapper
from queue import Queue
from utils.system import System
from utils.discord_api import DiscordAPI
from ui.ui import UIMain

def get_token():
    try:
        return os.environ["VISCORD_TOKEN"]
    except KeyError:
        print("You need to set the VISCORD_TOKEN environment variable to your token!")
        os._exit(1)

def start_client(client, token):
    try:
        client.run(token, bot = False)
    except AttributeError:
        print("Discord API fucked up again! DAMMIT")
    finally:
        os._exit(1)

class ViscordClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.loop_queue, self.ui_queue = Queue(maxsize=0), Queue(maxsize=0)
        self.discord_api = DiscordAPI(self, self.loop_queue, self.ui_queue)
        self.system = System()

    def start_ui(self):
        ui_main = UIMain(self.loop_queue, self.ui_queue)
        wrapper(ui_main.setup_ui)

    def start_loop(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.async_start_loop())

    async def async_start_loop(self):
        while True:
            await self.handle_queue_tasks()

    async def handle_queue_tasks(self):
        try:
            new_task = self.loop_queue.get(1)
            if new_task[0]:
                obj = getattr(self, new_task[0])
            else:
                obj = self
            func = getattr(obj, new_task[1])
            if inspect.iscoroutinefunction(func):
                try:
                    await func(*new_task[2])
                except IndexError:
                    await func()
            else:
                try:
                    func(*new_task[2])
                except IndexError:
                    func()
        except queue.Empty:
            return
        except TypeError:
            self.ui_queue.put(("bottom_bar", "change_text", ("Check the :help command to know how to use this command.",)))

    async def on_ready(self):
        ui_task = Thread(target=self.start_ui, name="ui_thread")
        ui_task.start()

        self.discord_api.api_loop = asyncio.get_running_loop()
        loop_task = Thread(target=self.start_loop, name="loop_thread")
        loop_task.start()

    async def on_message(self, msg):
        if msg.guild == self.discord_api.current_guild:
            if msg.channel == self.discord_api.current_channel:
                self.ui_queue.put(("chat_body", "add_to_chat_log", (msg,)))

client = ViscordClient()
token = get_token()
start_client(client, token)
