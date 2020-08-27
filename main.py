import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


bot = commands.Bot(command_prefix="><", case_insensitive=True)
bot.help_command = None

@bot.event
async def on_ready():
    print("And we're in")
    activity = discord.Activity(name="><help", type=discord.ActivityType.unknown)
    await bot.change_presence(activity=activity)

yes =os.getenv("key")
bot.run(yes)
