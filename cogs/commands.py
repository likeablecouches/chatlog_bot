import discord
from discord.ext import commands

from bot import bot

import os

logs_dir = 'logs'

# functions
def write_header(channel, file):
    file.write(f'Channel: {channel.name}\n'\
        + f'Guild: {channel.guild.name}\n'\
        + f'Category: {channel.category.name}\n\n'\
        #+ f'Created at: {channel.created_at[0:3]}\n\n')
        + '========================================\n\n')

def write_messages(mesg_list, file):
    for mesg in reversed(mesg_list):
        file.write(f'[{mesg.created_at}]\n'\
            + f'{mesg.author.display_name}({mesg.author.name}'\
            + f'#{mesg.author.discriminator}): {mesg.content}\n\n')

        if mesg.attachments:
            for attachment in mesg.attachments:
                file.write(f'{{Attachment(s)}}:\n'\
                    + f'Name:       {attachment.filename}\n'\
                    + f'Type:       {attachment.content_type}\n'\
                    + f'Size:       {attachment.size} byte(s)\n'\
                    + f'Url:        {attachment.url}\n\n')

def write_footer(mesg_num, file):
    file.write('========================================\n\n'\
        + f'Logged {mesg_num} messages(s)')

# class
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
    async def logchannel(self, ctx, channel_id=None, percentage=100, \
        filename=None):

        if channel_id == None:
            channel = ctx.channel
        else:
            channel = bot.get_channel(int(channel_id))

        if filename == None:
            filename = channel.name
        
        # converting percentage to decimal form for easier 
        # use without needing to convert it later on
        percentage = float(percentage) / 100
        
        messages = await channel.history(limit=None).flatten()

        if percentage < 1:
            messages = messages[:int(len(messages) * percentage)]

        if logs_dir not in os.listdir():
            oldmask = os.umask(000)
            os.mkdir(logs_dir, 0o755)
            os.umask(oldmask)
        
        with open(f'./{logs_dir}/{filename}', 'w') as logfile:
            # write channel info
            write_header(channel, logfile)
            write_messages(messages, logfile)
            write_footer(len(messages), logfile)

        with open(f'./{logs_dir}/{filename}', 'r') as logfile:
            await ctx.send(file=discord.File(fp=logfile, filename=filename))

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
