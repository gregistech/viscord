import discord

class DiscordAPI:
    def __init__(self, client, loop_queue, ui_queue):
        self.loop_queue, self.ui_queue = loop_queue, ui_queue
        self.client = client
        self.current_guild = None
        self.current_channel = None
    
    async def switch_to_channel(self, channel_name):
        if channel_name[0] == "#":
            channel_name = channel_name[1::]
        self.current_channel = discord.utils.get(self.current_guild.text_channels, name=channel_name)
        if self.current_channel:    
            self.ui_queue.put(("bottom_bar", "change_text", (f"You changed to channel #{self.current_channel.name}!",)))
        else:
            self.ui_queue.put(("bottom_bar", "change_text", (f"There are no channels named {channel_name}!",)))

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
            return
        self.ui_queue.put(("bottom_bar", "change_text", ("This guild is not available!",)))
    
    async def get_all_channels(self):
        if self.current_guild:
            channels = self.current_guild.text_channels
            channel_strings = []
            for x in channels:
                channel_strings.append(f"#{x.name}")
            self.ui_queue.put(("bottom_bar", "paginate_options", (channel_strings,)))
        else:
            self.ui_queue.put(("bottom_bar", "change_text", ("Select a guild first! (:guilds, :guild <identifier>)",)))

    async def get_all_guilds(self):
        guilds = self.client.guilds
        guild_strings = []
        count = 0
        for x in guilds:
            if not x.unavailable:
                guild_strings.append(f"{count} - {x.name}")
            count += 1
        self.ui_queue.put(("bottom_bar", "paginate_options", (guild_strings,)))

    async def send_message(self, channel_id, *message):
        await self.client.get_channel(int(channel_id)).send(" ".join(message))


