import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '.chatlog ')

@bot.event
async def on_ready():
    print('{0.user} is ready'.format(bot))

# test command
@bot.command()
async def makefile(ctx, name, text):
    with open(f'./user_files/{name}', 'w+') as user_file:
        user_file.write(text)

    with open(f'./user_files/{name}', 'r') as user_file:
        await ctx.send(file=discord.File(fp=user_file, filename=name))

# v load cogs below v

bot.run('ODYxOTQ4MDE4MTM5MjAxNTM2.YORNpQ.RiWo4OmodIypYegJUAL9iAahICQ')
        # ^ REMOVE TOKEN BEFORE COMMITING! ^
