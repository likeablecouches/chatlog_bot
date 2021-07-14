import discord
from discord.ext import commands

from bot import bot

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{bot} is ready')

def setup(bot):
    bot.add_cog(Events(bot))
