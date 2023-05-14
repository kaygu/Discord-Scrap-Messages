from colorama import Fore
import json
import os

import discord

DEFAULT_FOLDER_NAME = "logs"

client = discord.Client()

with open('config.json') as f:
    config = json.load(f)

def save_line(out, message):
    lines = []
    lines.append("{0}".format(message.author.name))
    lines.append("{0}".format(message.author.id))
    lines.append("{0}".format(message.created_at))
    lines.append("{0}".format(message.id))
    lines.append("{0}".format(message.content))
    atc_line = ""
    if message.attachments:
        for atch in message.attachments[:-1]:
            atc_line += atch.url + ", "
        atc_line += message.attachments[-1].url
    lines.append(atc_line)
    embed_line = ""
    if message.embeds:
        for embed in message.embeds[:-1]:
            embed_line += str(embed.to_dict()) + ", "
        embed_line += str(message.embeds[-1].to_dict())
    lines.append(embed_line)
     

    for line in lines:
        out.write(line + ";")
    out.write('\n')
    

async def get_logs(channel: discord.TextChannel):
    try:
        print(f"\n{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Gettings message history for {Fore.WHITE}{channel.name}")
        with open("{0}/{1}_{2}_{3}.csv".format(config.get("log_folder", DEFAULT_FOLDER_NAME), channel.guild.name, channel.name, channel.id), 'w', encoding="utf-8") as f:
            async for line in channel.history(limit=config.get("amount"), oldest_first=True):
                save_line(f, line)

        print(f"{Fore.WHITE}[ {Fore.YELLOW}@ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Messages for channel {Fore.WHITE}{channel.name} {Fore.LIGHTBLACK_EX}finished downloading")
    except Exception as e:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.WHITE}{e}")

def Init():
    try:
        os.mkdir(config.get("log_folder", DEFAULT_FOLDER_NAME))
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
    channels = []
    try:
        guild = client.get_guild(guild_id)
        if not guild:
            raise Exception("Guild ID is invalid")
        channels = guild.text_channels
        for channel_id in channel_ids:
            channel = client.get_channel(channel_id)
            if not channel:
                raise Exception("Channel ID is invalid")
            if channel not in channels:
                channels.append(channel)
        for channel in channels:
            await get_logs(channel)
    except Exception as e:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.WHITE}{e}")
    await client.close()
    
    

if __name__ == '__main__':    
    os.system('cls')

    print(f"\n{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Bot is ready!")

    Init()
