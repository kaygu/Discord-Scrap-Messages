from colorama import Fore
import json

import discord

with open('config.json') as f:
    config = json.load(f)

LOG_FOLDER = config.get("log_folder", "logs")
CSV_SEP = config.get("csv_separator", "\t")

def message_to_csv(message: discord.Message):
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

def save_line(out, message: discord.Message):
    # TODO: Batch file writing
    # TODO: Change file every x messages to avoid files with gigabytes of data
    # with open("{0}/{1}_{2}_{3}.csv".format(LOG_FOLDER, message.channel.guild.name, message.channel.name, message.channel.id), 'w', encoding="utf-8") as f:
    out.write(message_to_csv(message))
    