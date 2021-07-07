import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '.chatlog ')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
