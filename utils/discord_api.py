import discord
import asyncio

class DiscordAPI:
    def __init__(self, client, loop_queue, ui_queue):
        self.loop_queue, self.ui_queue = loop_queue, ui_queue
        self.api_loop = None
        self.client = client
        self.current_guild = None
        self.current_channel = None
    
    async def get_current_channel_history(self, limit = 100):
        try:
            history = await self.current_channel.history(limit=limit).flatten()
        except discord.errors.Forbidden:
            history = None
        finally:
            return history
    async def switch_to_channel(self, channel_name):
        self.current_channel = None
        if self.current_guild:
            if channel_name == None:
                self.ui_queue.put(("chat_body", "set_chat_log", (None,)))
            if channel_name[0] == "#":
                channel_name = channel_name[1::]
            writeable_channels = []
            for x in self.current_guild.text_channels:
                name = x.name.encode("ascii", errors="ignore").decode()
                if name == channel_name:
                    self.current_channel = x
            if self.current_channel:
                channel_history = asyncio.run_coroutine_threadsafe(self.get_current_channel_history(), self.api_loop).result()
                if channel_history:
                    self.ui_queue.put(("chat_body", "set_chat_log", (channel_history,)))
                    self.ui_queue.put(("bottom_bar", "change_text", (f"You changed to channel #{self.current_channel.name}!",)))
                    self.ui_queue.put(("top_bar", "change_text", (f"#{self.current_channel.name} - {self.current_guild.name}",)))
                else:
                    self.ui_queue.put(("bottom_bar", "change_text", (f"Couldn't get channel history, not switching!",)))
                    self.ui_queue.put(("top_bar", "change_text", (f"Not in a channel - {self.current_guild.name}",)))
                    self.current_channel = None
            else:
                self.ui_queue.put(("bottom_bar", "change_text", (f"There are no channels named {channel_name}!",)))
        else:
            self.ui_queue.put(("bottom_bar", "change_text", ("Select a guild first! (:guilds, :guild <identifier>)",)))

    async def switch_to_guild(self, identifier, identifier_type = "count"):
        try:
            if identifier_type == "count":
                guild = self.client.guilds[int(identifier)]
        except IndexError:
            self.ui_queue.put(("bottom_bar", "change_text", ("You are not joined to this guild!",)))
            return
        if guild and not guild.unavailable:
            self.current_guild = guild
            self.ui_queue.put(("bottom_bar", "change_text", (f"You changed to guild {guild.name}!",)))
            self.ui_queue.put(("top_bar", "change_text", (f"Not in channel - {self.current_guild.name}",)))
            return
        self.ui_queue.put(("bottom_bar", "change_text", ("This guild is not available!",)))

    async def get_all_channels(self):
        if self.current_guild:
            channels = self.current_guild.text_channels
            channel_strings = []
            for x in channels:
                name = x.name.encode("ascii", errors="ignore").decode()
                channel_strings.append(f"#{name}")
            self.ui_queue.put(("bottom_bar", "paginate_options", (channel_strings,)))
        else:
            self.ui_queue.put(("bottom_bar", "change_text", ("Select a guild first! (:guilds, :guild <identifier>)",)))

    async def get_all_guilds(self):
        guilds = self.client.guilds
        guild_strings = []
        count = 0
        for x in guilds:
            if not x.unavailable:
                name = x.name.encode("ascii", errors="ignore").decode()
                guild_strings.append(f"{count} - {name}")
            count += 1
        self.ui_queue.put(("bottom_bar", "paginate_options", (guild_strings,)))

    async def send_message(self, message):
        if self.current_channel:
            try:
                asyncio.run_coroutine_threadsafe(self.current_channel.send(message), self.api_loop).result()
            except discord.errors.HTTPException:
                self.ui_queue.put(("bottom_bar", "change_text", ("You can't send an empty message!",)))
        else:
            self.ui_queue.put(("bottom_bar", "change_text", ("Select a channel first! (:channels, :channel <channel_name>)",)))
