from colorama import Fore
import json
import os

import discord

client = discord.Client()

with open('config.json') as f:
    config = json.load(f)

LOG_FOLDER = config.get("log_folder", "logs")
CSV_SEP = config.get("csv_separator", "\t")

def extract_message(message):
    # TODO: Escape special characters
    # TODO: Other options than CSV. json should be a feature next
    line = []
    values = []
    values.append("{0}".format(message.author.name))
    values.append("{0}".format(message.author.id))
    values.append("{0}".format(message.created_at))
    values.append("{0}".format(message.id))
    values.append("{0}".format(message.content))
    atc_val = []
    if message.attachments:
        for atch in message.attachments:
            atc_val.append(atch.url)
    values.append(json.dumps(atc_val))
    embed_val = []
    if message.embeds:
        for embed in message.embeds:
            embed_val.append(embed.to_dict())
    values.append(json.dumps(embed_val))
     

    for val in values:
        line.append(val + CSV_SEP)
    line.append('\n')
    return "".join(line)

def save_line(out, message):
    # TODO: Batch file writing
    # TODO: Change file every x messages to avoid files with gigabytes of data
    out.write(extract_message(message))
    

async def get_logs(channel: discord.TextChannel):
    try:
        print(f"\n{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Gettings message history for {Fore.WHITE}{channel.name}")
        with open("{0}/{1}_{2}_{3}.csv".format(LOG_FOLDER, channel.guild.name, channel.name, channel.id), 'w', encoding="utf-8") as f:
            async for line in channel.history(limit=config.get("amount"), oldest_first=True):
                save_line(f, line)

        print(f"{Fore.WHITE}[ {Fore.YELLOW}@ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Messages for channel {Fore.WHITE}{channel.name} {Fore.LIGHTBLACK_EX}finished downloading")
    except Exception as e:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.WHITE}{e}")

def Init():
    try:
        os.mkdir(LOG_FOLDER)
    except FileExistsError:
        pass
    if not config.get('token'):
        os.system('cls')
        print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}No token in config.json\n\n"+Fore.RESET)
        exit()
    elif not config.get("guild") and not config.get("channels"):
        os.system('cls')
        print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}No guild or channel in config.json\n\n"+Fore.RESET)
        exit()
    else:
        token = config.get('token')
        try:
            client.run(token)
        except discord.errors.LoginFailure:
            print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Token is invalid\n\n"+Fore.RESET)
            exit()

@client.event
async def on_ready():
    print(f'{Fore.LIGHTBLACK_EX}We have logged in as {client.user}')
    guild_id = config.get("guild")
    channel_ids = config.get("channels")
    global channels # Shame on me, but this is the only way I found until I rewrite my script 
    channels = []
    try:
        if guild_id:
            guild = client.get_guild(guild_id)
            if not guild:
                raise Exception("Guild ID is invalid")
            channels = guild.text_channels
        if channel_ids:
            for channel_id in channel_ids:
                channel = client.get_channel(channel_id)
                if not channel:
                    raise Exception("Channel ID is invalid")
                if channel not in channels:
                    channels.append(channel)
                else:
                    print(f"\n{Fore.WHITE}[ {Fore.YELLOW}W {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Channel ID {Fore.WHITE}{channel} {Fore.LIGHTBLACK_EX}is already in the channel list\n")
        for channel in channels:
            await get_logs(channel)
    except Exception as e:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.WHITE}{e}")

@client.event
async def on_message(message):
    # Live Listener
    # TODO: Save messages here, but only once logs history is gathered (so no duplicates)
    if message.channel in channels:
        # Log message here
        print(f"{Fore.WHITE}[ {Fore.GREEN}@ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Messages in channel {Fore.WHITE}{message.channel.name} {Fore.LIGHTBLACK_EX}recieved")
    
    

if __name__ == '__main__':    
    os.system('cls')

    print(f"\n{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Bot is ready!")

    Init()
