import discord
from discord.ext import commands
import asyncio
import math
from kobj import *
from ktemplate import templatelist, paradelist
from random import randint
import random
import re


class objcommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        TheWorld.exists = True

    cusobjlist = []

    # Commands

    @commands.command()
    async def create(self, ctx, objtomake=None):
        if objtomake is None:
            await ctx.send("""Creating objects is simple.
Tell me what you want to create, and tell me the information in key value pairs. 
For example: Say you are creating a chair, to set the number of legs, you can do numberoflegs=4.
You can tell me ANYTHING, the only limit is that each item can only have a max of 20 not including Name values. Use >>>example for an example""")
            return

        tomake = [x for x in templatelist if objtomake.lower() == x.name.lower()]
        if not tomake:
            await ctx.send("I can't seem to find that. Use <>template to view a list")
            return
        
        else:
            await self.getname(ctx, tomake)

    @commands.command()
    async def template(self, ctx, param=None):
        if param is None:
            tempbed = discord.Embed(
                title="Template List",
                color=randint(0, 0xffffff)
            )
            for template in templatelist:
                tempbed.add_field(name=f'Name: {template.name}', value=f"Description: {template.desc}. Category: {template.category}")

            await ctx.send(tempbed)
            return

    @commands.command()
    async def example(self, ctx):
        await ctx.send("It was requested and therefore it will be granted. Here is an example")
        await ctx.send(">>>create creature")
        await ctx.send("```Ok, Begin by telling me it's name```")
        await ctx.send("name=Jerry_The_Beast")
        await ctx.send("```Good, now tell me any attributes of Jerry_The_Beast that you want```")
        await ctx.send("age=1004")
        await ctx.send("description=very scary")
        await ctx.send("Done")
        await ctx.send("```Completed. View with >>>mycreations```")


    # Functions

    async def getname(self, ctx, objtomake):
        await ctx.send("You will give me the information on your creation in key=value format. Begin by telling me it's name")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
        except TimeoutError:
            await ctx.send("You took too long to respond")
            return

        if len(msg.content) > 35:
            await ctx.send("Cannot be more than 35 characters")
            return

        if " " in msg.content:
            await ctx.send("Refrain from using spaces. Use _ or - instead")
            return

        thename = re.findall(r"name=(\S+?)", msg.content)
        if not thename:
            await ctx.send("Did not get the name. Try again. format is name=the_name_you_want")
            return

        _vname = thename[0]
        _objtomake = objtomake.capitalize()
        _iditem = await self.getid(ctx)
        userobj = eval("objtomake(True, ctx.author.id, ctx.author.name, _iditem, _objtomake, _vname")
        await self.creating(ctx, userobj)

    async def getid(self, ctx):
        iid = [x.itemid for x in self.cusobjlist if x.userid == ctx.author.id]
        if iid:
            iid.sort(reverse=True)
            highestid = iid[0]
            return highestid + 1
        else:
            return 0

    async def creating(self, ctx, objmaking):
        await ctx.send(f"""Excellent, Now go ahead and tell me more about {objmaking.name}. Remember to use key=value format
As a side note, you can overwrite a previous value using key=different_value. Type anything without an '=' when you are done""")

        counter = 1

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        while counter < 21:
            await ctx.send("I'm listening")
            try:
                msg = self.bot.wait_for("message", timeout=90, check=check)
            except:
                await ctx.send("You took too long to respond and I lost interest 😓. Try again later")
                return

            if "=" not in msg:
                await ctx.send("Ending Early")
                break

            if " " in msg:
                await ctx.send("Your key=value must not have in spaces. Use _ or - instead")
                continue
            attri = re.findall(r"(\S+)=(\S+)", msg)
            if attri:
                attri = attri[0]
                key = attri[0]
                value = attri[1]

            else:
                await ctx.send("That did not match the key=value format I told you to use 🏋️‍♂️")
                continue

            setattr(objmaking, key, value)
            counter += 1

        await ctx.send("Completed. View with >>>mycreation")
        self.cusobjlist.append(objmaking)


    # Events

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):

            await ctx.send(f"You are on Cooldown for {math.floor(error.retry_after)} seconds")

        if isinstance(error, commands.MissingPermissions):
            
            await ctx.send(error)
        
        if isinstance(error, commands.CommandNotFound):
            
            await ctx.send(error)

        if isinstance(error, commands.NotOwner):
            
            await ctx.send(error)

        if isinstance(error, commands.MissingRequiredArgument):
            
            await ctx.send(error)         

        else:
            channel = self.bot.get_channel(740337325971603537)
            await channel.send(f"{ctx.author.name}: {error}")
            print(error)


def setup(bot):
    bot.add_cog(objcommands(bot))