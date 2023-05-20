from colorama import Fore
import json
import datetime
import os

import discord

LOG_TRACE = "trace.json"
LOGS_PER_FILE = 5000 #Number of lines per CSV file
MIN_DELAY_BETWEEN_SAVES = 90 # in seconds

class Parser:
    def __init__(self, config):
        self.batch = {}

        self.trace = []
        if os.path.exists(LOG_TRACE):
            with open(LOG_TRACE, 'r') as f:
                try:
                    self.trace = json.load(f)
                except json.decoder.JSONDecodeError:
                    print(f"{Fore.RED}JSON ERROR")

        self.LOG_FOLDER = config.get("log_folder", "logs")
        self.CSV_SEP = config.get("csv_separator", "\t")            

        
    def message_to_csv(self, message: discord.Message):
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
            line.append(val + self.CSV_SEP)
        line.append('\n')
        return "".join(line)

    def save_line(self, message: discord.Message):
        
        # Create batch key if None
        if not self.batch.get(str(message.channel.id)):
            self.first_msg_date = int(message.created_at.timestamp())
            self.batch[str(message.channel.id)] = []
            
        self.batch[str(message.channel.id)].append(self.message_to_csv(message)) # Add message to batch
        self.set_channel_trace(message) #Update trace with latest info

        # Check if batch should be saved to file
        if len(self.batch.get(str(message.channel.id), [])) >= LOGS_PER_FILE -1 or\
            datetime.datetime.now().timestamp() - self.get_channel_trace(message.channel).get("last_save_ts") > MIN_DELAY_BETWEEN_SAVES:
            self.first_msg_date = int(message.created_at.timestamp())
            self.save_batch(message.channel)
  

    def save_batch(self, channel):
        trace = self.get_channel_trace(channel)
        filename = trace.get("filename")
        trace["last_save_ts"] = datetime.datetime.now().timestamp()
        nb_msgs = trace.get("nb_logs", 0)
        
        if not filename:
            filename = "{0}/{1}_{2}_{3}.csv".format(self.LOG_FOLDER, channel.guild.name, channel.name, self.first_msg_date)
            trace["filename"] = filename
        if nb_msgs >= LOGS_PER_FILE -1:
            trace["nb_logs"] = 0
        
        if self.batch.get(str(channel.id)):
            print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Batch was written in file {Fore.WHITE}{filename}\n")
            with open(filename, 'a+', encoding="utf-8") as f:
                f.write("".join(self.batch[str(channel.id)]))
            with open(LOG_TRACE, 'w') as f:
                json.dump(self.trace, f)
        self.batch[str(channel.id)] = [] # Reset batch
            
    def get_trace(self) -> list:
        return self.trace
    
    def get_channel_trace(self, channel: discord.TextChannel) -> dict:   
        default = {'channel': channel.id, 'last_message': None, 'filename': "", 'nb_logs': 0, "last_save_ts": datetime.datetime.now().timestamp()}     
        try:
            trace = next((item for item in self.trace if item.get("channel") == channel.id))
            return trace
        except StopIteration:
            self.trace.append(default)
            return default
    
    def get_channel_trace_index(self, channel: discord.TextChannel) -> int:
        for i, d in enumerate(self.trace):
            if d["channel"] == channel.id:
                return i
  
    def set_channel_trace(self, message: discord.Message):
        channel_trace = self.trace.pop(self.get_channel_trace_index(message.channel))
        channel_trace["last_message"] = message.id
        channel_trace["nb_logs"] += 1
        # channel_trace["last_log_ts"] = message.created_at.timestamp()
        self.trace.append(channel_trace)
    

    '''
    trace structure:
    [
      {
        "channel": 
        "last_message": 202514,
        "filename": "",
        "nb_logs": 0,
        "last_log_ts": 
      },
    ]
    
    '''