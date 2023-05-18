from colorama import Fore
import json
import discord
import datetime

from utils import parser

LOG_TRACE = "trace.json"

class MyClient(discord.Client):
    def __init__(self, config):
        super().__init__()
        self.channels = [] # List of channels to get history
        self.channels_to_listen = [] # List of channels to listen to new messages
        self.guild_ids = config.get('guilds')
        self.channel_ids = config.get('channels')
        self.amount = config.get('amount') # Amount of messages to retrieve per channel

        self.LOG_FOLDER = config.get("log_folder", "logs")
        with open(LOG_TRACE, 'r') as f:
            try:
                self.trace = json.load(f)
            except json.decoder.JSONDecodeError:
                self.trace = {}

    async def on_ready(self):
        print(f'{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}We have logged in as {Fore.WHITE}{self.user}')
        try:
            if self.guild_ids:
                for guild_id in self.guild_ids:
                    guild = self.get_guild(guild_id)
                    if not guild:
                        raise Exception(f"Guild ID {guild_id} is invalid")
                    self.channels += guild.text_channels
            if self.channel_ids:
                for channel_id in self.channel_ids:
                    channel = self.get_channel(channel_id)
                    if not channel:
                        raise Exception(f"Channel ID {channel_id} is invalid")
                    if channel not in self.channels:
                        self.channels.append(channel)
                    else:
                        print(f"\n{Fore.WHITE}[ {Fore.YELLOW}W {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Channel ID {Fore.WHITE}{channel} {Fore.LIGHTBLACK_EX}is already in the channel list\n")
        except Exception as e:
            print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.WHITE}{e}")
        for channel in self.channels:
            await self.get_logs(channel)
    
    async def on_message(self, message):
        # TODO: Save messages here, but only once logs history is gathered (so no duplicates)
        if message.channel in self.channels_to_listen:
            print(f"\n{Fore.WHITE}[ {Fore.GREEN}@ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Messages in channel {Fore.WHITE}{message.channel.name} {Fore.LIGHTBLACK_EX}recieved")
            print(message.content)

    async def get_logs(self, channel: discord.TextChannel):
        print(f"\n{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Gettings message history for {Fore.WHITE}{channel.name}")
        try:
            msg_id = self.trace.get(str(channel.id))
            last_msg = await channel.fetch_message(msg_id)
        except discord.NotFound:
            last_msg = None
            print(f"\n{Fore.WHITE}[ {Fore.YELLOW}W {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Message ID {Fore.WHITE}{msg_id} {Fore.LIGHTBLACK_EX} was not found for channel {Fore.WHITE}{channel.name} ({channel.id})\n")
        except discord.errors.Forbidden as e:
            print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Forbidden: {Fore.WHITE}{e}")
            return
        try:
            with open("{0}/{1}_{2}_{3}.csv".format(self.LOG_FOLDER, channel.guild.id, channel.name, datetime.datetime.now().timestamp()), 'w', encoding="utf-8") as f:
                async for line in channel.history(after=last_msg, oldest_first=True, limit=self.amount):
                    parser.save_line(f, line)
                    self.trace[str(channel.id)] = line.id
            self.channels_to_listen.append(channel)
            with open(LOG_TRACE, 'w') as f:
                json.dump(self.trace, f)
            

            print(f"{Fore.WHITE}[ {Fore.YELLOW}@ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Messages for channel {Fore.WHITE}{channel.name} {Fore.LIGHTBLACK_EX}finished downloading")
        except Exception as e:
            print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.WHITE}{e}")
