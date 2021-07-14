import discord
from discord.ext import commands

from bot import bot

import os

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # reference command
    @commands.command()
    async def makefile(self, ctx, name, text):
        with open(f'./user_files/{name}', 'w+') as user_file:
            user_file.write(text)

        with open(f'./user_files/{name}', 'r') as user_file:
            await ctx.send(file=discord.File(fp=user_file, filename=name))

    @commands.command()
    async def clear(self, ctx, amount=10):
        if amount == 'all':
            await ctx.channel.purge(limit=None)
        else:
            await ctx.channel.purge(limit=int(amount))

    @commands.command()
    async def logchannel(self, ctx, channel_id, percentage=100, \
        filename=None):

        channel = bot.get_channel(int(channel_id))

        if filename == None:
            filename = channel.name
        
        # converting percentage to decimal form for easier 
        # use without needing to convert it later on
        percentage = float(percentage) / 100
        
        messages = await channel.history(limit=None).flatten()
        
        logs_dir = 'logs'

        if percentage < 1:
            messages = messages[:int(len(messages) * percentage)]

        if logs_dir not in os.listdir():
            os.mkdir(logs_dir, 755)

        '''
            1. set channel var to channel object by channel id
            2. if filename not passed, set filename to name of channel 
            3. set messages var to list of {percentage}% of channel messages
            4. if tmp dir does not exist, create it
            5. create log file in tmp dir for writing and reading 
            6. write all messages(sender, time sent, contents)
            in {messages} to log file
            7. send log file
            8. close log file
            9. delete log file
        '''

def setup(bot):
    bot.add_cog(Commands(bot))
