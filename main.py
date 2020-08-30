import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


bot = commands.Bot(command_prefix=">>>", case_insensitive=True)
bot.help_command = None

bot.load_extension("objcom")
bot.load_extension("myhelp")

@bot.event
async def on_ready():
    print("And we're in")
    activity = discord.Activity(name=">>>help", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.command()
@commands.is_owner()
async def refresh(ctx):
    bot.reload_extension("objcom")
    bot.reload_extension("myhelp")

yes=os.getenv("key")
bot.run(yes)
