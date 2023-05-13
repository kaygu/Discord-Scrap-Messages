from colorama import Fore
import json
import os

import discord
from discord.ext import commands, tasks


client = discord.Client()

with open('config.json') as f:
    config = json.load(f)


def Init():
    if not config.get('token'):
        os.system('cls')
        print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}You didnt put your token in the config.json file\n\n"+Fore.RESET)
        exit()
    else:
        token = config.get('token')
        try:
            client.run(token)
            os.system(f'Discord message scraper')
        except discord.errors.LoginFailure:
            print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Token is invalid\n\n"+Fore.RESET)
            exit()


# @client.command()
# async def scrape(ctx:  commands.Context, amount: int):
#     f = open(f"scraped/{ctx.message.channel}.txt","w+", encoding="UTF-8")
#     total = amount
#     print(f"{Fore.WHITE}[ {Fore.YELLOW}? {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Scraping {Fore.WHITE}{amount}{Fore.LIGHTBLACK_EX} messages to {Fore.WHITE}scraped/{ctx.message.channel}.txt{Fore.LIGHTBLACK_EX}!")
#     async for message in ctx.message.channel.history(limit=amount):
#         attachments = [attachment.url for attachment in message.attachments if message.attachments]
#         try:
#             if attachments:
#                 realatt = attachments[0]
#                 f.write(f"({message.created_at}) {message.author}: {message.content} ({realatt})\n")
#                 print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Scraped message")
#             else:
#                 f.write(f"({message.created_at}) {message.author}: {message.content}\n")
#                 print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Scraped message")
#         except Exception as e:
#             print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Cannot scrape message from {Fore.WHITE}{message.author}")
#             print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX} {Fore.WHITE}{e}")
#             total = total - 1
#     print(f"{Fore.WHITE}[ {Fore.YELLOW}? {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Succesfully scraped {Fore.WHITE}{total} {Fore.LIGHTBLACK_EX}messages!\n\n{Fore.WHITE}")


@client.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, discord.errors.Forbidden):
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Discord error: {error}"+Fore.RESET)    
    else:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}{error_str}"+Fore.RESET)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}{message.channel.name}")
    print(f"{Fore.WHITE}[ {Fore.CYAN}{message.channel.name} {Fore.WHITE}] {Fore.LIGHTBLACK_EX}{message.content}")

if __name__ == '__main__':    
    os.system('cls')

    print(f"\n{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Bot is ready!")

    Init()
    # 1) Scrap channel history
    # 2) Read Logs constantly 