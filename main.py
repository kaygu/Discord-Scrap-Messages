from colorama import Fore
import json
import os
import discord

from utils.client import MyClient

with open('config.json') as f:
    config = json.load(f)

LOG_FOLDER = config.get("log_folder", "logs")
CSV_SEP = config.get("csv_separator", "\t")

def Init():
    try:
        os.mkdir(LOG_FOLDER)
    except FileExistsError:
        pass
    if not config.get('token'):
        os.system('cls')
        print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}No token in config.json\n\n"+Fore.RESET)
        exit()
    elif not config.get("guilds") and not config.get("channels"):
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

if __name__ == '__main__':
    client = MyClient(config)
    Init()