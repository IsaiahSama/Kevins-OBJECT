import discord
from discord.ext import commands, tasks
import asyncio
import math
from kobj import *
from ktemplate import templatelist, paradelist
from random import randint
import random
import re
import json
from os import path


class objcommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        TheWorld.exists = True
        self.save.start()

    if path.exists("customobjects.json"):
        with open("customobjects.json") as p:
            cusdictlist = json.load(p)
    else:
        cusdictlist = []

    cusobjlist = []
    rwords = ["itemid", "userid", "username", "exists", "objtype"]

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
            await ctx.send("I can't seem to find that. Use >>>template to view a list")
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

    @commands.command()
    async def mycreations(self, ctx):
        usercreations = [dic for dic in self.cusdictlist if dic["userid"] == ctx.author.id]
        if not usercreations:
            await ctx.send("You have not created any items as yet. Get started with >>>help")
            return

        tosend = []
        for creation in usercreations:
            tosend.append(f"Name: {creation['name']}, ID: {creation['itemid']}, Object Type: {creation['objtype']}\n")
        
        await ctx.send(f"Here is a list of all of your items: {', '.join(tosend)}")
        await ctx.send("You can view more information with >>>view itemid. Using the name will return the first match. Not just yours")

    
    @commands.command()
    async def view(self, ctx, idtoview):
        itemtoview = [x for x in self.cusdictlist if idtoview == x["itemid"] or idtoview == x["name"]]
        if itemtoview:
            itv = itemtoview[0]
            embed = discord.Embed(
                title="Viewing Object",
                description=f"Showing {itv['username']}'s {itv['objtype']}",
                color=randint(0, 0xffffff)
            )

            for k, v in itv:
                embed.add_field(name=k, value=v)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Could not find any item with that ID")
            return

    
    @commands.command()
    async def update(self, ctx, idtoupdate=None):
        try:
            itu = int(idtoupdate)
        except ValueError:
            await ctx.send("The ID must be a number")
            return

        allo = await self.getuserobj(ctx.author.id)
        if allo is None:
            await ctx.send("You don't seem to own any objects. Use >>>help for more information")
            return
        
        otu = [uobj for uobj in allo if uobj["itemid"] == itu]
        
        if otu is None:
            await ctx.send("That ID does not match any of your Objects")
            return
        
        otu = otu[0]

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            await ctx.send(f"What about {otu['name']} do you wish to change? Keys? Values? or Pairs?. Type keys, values or pairs.")
            try:
                tochange = self.bot.wait_for("message", timeout=30, check=check)
            except TimeoutError:
                await ctx.send("Took too long. Aborting operation, woop woop.")
                return

            if tochange.content.lower() not in ["keys", "values", "pairs"]:
                await ctx.send("That is not keys, values or pairs. If you wish to exit, stay quiet for 30 seconds")
                continue

            break
        
        await self.view(ctx, itu)
        if tochange.content.lower() == "keys":
            await self.changekey(ctx, otu)
        elif tochange.content.lower() == "values":
            await self.changevalue(ctx, otu)
        elif tochange.content.lower() == "pairs":
            await self.changepair(ctx, otu)
        else:
            await ctx.send("Something went wrong. Try again later")

    @commands.command()
    async def delete(self, ctx, idtodelete, conf=False):
        itemtodelete = [obj for obj in self.cusdictlist if obj["itemid"] == idtodelete and obj["userid"] == ctx.author.id]

        if itemtodelete:
            itd = itemtodelete[0]
            if not conf:
                await ctx.send(f"This will delete this item permanately. Do >>>delete {idtodelete} True to confirm")
                return

            await ctx.send(f"Deleting {itd.name}")
            del itd
            await ctx.send("Successful, for I have devoured it :yum:")
        else:
            await ctx.send("I could not find any item belonging to you with that ID")
            return

    # Functions

    async def changekey(self, ctx, otu):
        await ctx.send("Which key would you like to change?")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            try:
                ktc = self.bot.wait_for("message", timeout=60, check=check)
            except TimeoutError:
                await ctx.send("Took too long... aborting ;p")
                return

            ktc = ktc.content
            if ktc.startswith(">>>"): continue

            nktc = [key for key in otu.keys() if key.lower() == ktc.lower()]
            
            if nktc:
                await ctx.send("I have found that key")
                break
            else:
                await ctx.send("I did not find that key. Try again please")
                continue
        
        while True:
            await ctx.send(f"What would you like to change {nktc} to?")
            try:
                resp = self.bot.wait_for("message", timeout=60, check=check)
            except TimeoutError:
                await ctx.send("Sigh... Taking a bit too long to answer a relativel simple question... :yawning_face:")
                return
            
            resp = resp.content
            if ' ' in resp:
                await ctx.send("Your key can not have in a space. use _ or - instead")
                continue

            if len(resp) > 15:
                await ctx.send("Your key cannot be more than 15 charactes")
                continue
                
            break

        otu[resp] = otu[nktc]
        del otu[nktc]

        await ctx.send("Successful")


    async def changevalue(self, ctx, otu):
        await ctx.send("Which key would you like to change the value of?")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            try:
                ktc = self.bot.wait_for("message", timeout=60, check=check)
            except TimeoutError:
                await ctx.send("Took too long... aborting ;p")
                return

            ktc = ktc.content
            if ktc.startswith(">>>"): continue

            nktc = [key for key in otu.keys() if key.lower() == ktc.lower()]
            
            if nktc:
                await ctx.send("I have found that key")
                break
            else:
                await ctx.send("I did not find that key. Try again please")
                continue

        await ctx.send(f"The value for {nktc} is {otu[nktc]}")
        while True:
            await ctx.send("What would you like to change this value to?")

            try:
                tochange = await self.bot.wait_for("message", timeout=60, check=check)
            except TimeoutError:
                await ctx.send(":yawning_face: Goodbye")
                return

            tc = tochange.content
            if len(tc) > 50:
                await ctx.send("Your value cannot be more than 50 characters")
                continue
            
            break

        otu[nktc] = tc
        await ctx.send("Completed")

    
    async def changepair(self, ctx, otu):
        await self.changekey(ctx, otu)
        await self.changevalue(ctx, otu)           


    async def getuserobj(self, ownerid):
        toreturn = [x for x in self.cusdictlist if x["userid"] == ownerid]
        
        if toreturn:
            return toreturn
        
        return None

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

        thename = re.findall(r"name=(.+?)", msg.content)
        if not thename:
            await ctx.send("Did not get the name. Try again. Format is name=the_name_you_want")
            return

        _vname = thename[0]
        _objtomake = objtomake.capitalize()
        _iditem = await self.getid(ctx)
        userobj = eval("objtomake(True, ctx.author.id, ctx.author.name, _iditem, _objtomake, _vname")
        await self.creating(ctx, userobj)

    async def getid(self, ctx):
        iid = [x["itemid"] for x in self.cusdictlist]
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
            await ctx.send("Speak, I'm listening")
            try:
                msg = self.bot.wait_for("message", timeout=90, check=check)
            except:
                await ctx.send("You took too long to respond and I lost interest 😓. Try again later")
                return

            msg = msg.content

            if "=" not in msg:
                if counter == 1:
                    await ctx.send("Cancelling")
                    return
                else:
                    await ctx.send("Finishing up")
                    break

            attri = re.findall(r"(\S+)=(.+)", msg)
            if attri:
                attri = attri[0]
                key = attri[0]
                if key.lower() in self.rwords:
                    await ctx.send("You cannot use That as a key because it is a reserved word")
                    continue
                if " " in key:
                    await ctx.send("Your key must not have in spaces. Use _ or - instead")
                    continue

                if len(key) > 15:
                    await ctx.send("Your key should not be more than 15 characters")

                value = attri[1]
                if len(value) > 50:
                    await ctx.send("Your value cannot be more than 50 characters")

            else:
                await ctx.send("That did not match the key=value format I told you to use 🏋️‍♂️")
                continue

            setattr(objmaking, key, value)
            counter += 1

        await ctx.send("Completed. View with >>>mycreations")
        self.cusobjlist.append(objmaking)
        self.cusdictlist.append(objmaking.__dict__)

    
    async def getobj(self, objtoget):
        _typeobj = objtoget["objtype"]
        p = objtoget
        objtoreturn = eval("typeobj(p['exists'], p['userid'], p['username'], p['itemid'], p['objtype'], p['name'])")
        
        for k, v in p.items():
            setattr(objtoreturn, k, v)

        return objtoreturn
    

    @tasks.loop(minutes=2)
    async def save(self):
        if len(self.cusdictlist) > 0:
            with open("customobjects.json", "w") as f:
                json.dump(self.cusdictlist, f, indent=4)

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
            print(error)


def setup(bot):
    bot.add_cog(objcommands(bot))
