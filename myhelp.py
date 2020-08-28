import discord
from discord.ext import commands
import asyncio
from myhelpclass import cmdlist
from random import randint

class myhelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, param=None):
        if param == None:
            embed = discord.Embed(
                title="Help",
                description=f"Showing help for {ctx.author.name}",
                color=randint(0, 0xffffff)
            )

            embed.set_thumbnail(url=self.bot.avatar_url)
            embed.add_field(name="Basic Information:", value="""
    I function using the CRUD principle, meaning Create, Read, Update and Delete.
    As such, I will allow you to create your objects, view them, update them and delete them as you see fit""")
            embed.add_field(name=">>>commandlist", value="You can use >>>commandlist to view my commands")
            embed.add_field(name="Extra Information", value="All items you create only require a name. Everything else is your choice")
            embed.add_field(name="Other Commands", 
            value="""If you wish to create an item that may be implemented into the bot itself, It has to follow a certain format.
Templates that can be implemented into the bot itself will be marked with <> followed by the category name.
You can use these same templates like you would the others, and make your own custom stuff, but to make one compatible with the bot...
You'll have to do >>>template templatename to get the format. I look forward to seeing what you create""")

            await ctx.send(embed=embed)
            return
        
        cmdtoget = [cmd for cmd in cmdlist if param.lower() in cmd.name.lower() or 
        param.lower() in cmd.desc.lower()]

        if not cmdtoget:
            await ctx.send("That command could not be found. You can use >>>commandlist for a list")
            return
        
        helpbed = discord.Embed(
            title="Command List",
            color=randint(0, 0xffffff)
        )

        for cmd in cmdtoget:
            helpbed.add_field(name=cmd.name, value=f"Usage: {cmd.usage}- Description: {cmd.desc}")

        await ctx.send(embed=helpbed)


    @commands.command()
    async def commandlist(self, ctx):
        helpbed = discord.Embed(
            title="Command List",
            color=randint(0, 0xffffff)
        )

        for cmd in cmdlist:
            helpbed.add_field(name=cmd.name, value=cmd.usage)

        await ctx.send(embed=helpbed, content="Use >>>help commandname for more information")


def setup(bot):
    bot.add_cog(myhelp(bot))
