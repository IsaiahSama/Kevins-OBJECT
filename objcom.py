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
import traceback


class objcommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        TheWorld.exists = True
        self.save.start()

    if path.exists("customobjects.json"):
        with open("customobjects.json") as p:
            custom_dict_list = json.load(p)
    else:
        custom_dict_list = []

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
            await self.getname(ctx, objtomake)

    @commands.command()
    async def template(self, ctx, param=None):
        if param is None:
            tempbed = discord.Embed(
                title="Template List",
                color=randint(0, 0xffffff)
            )
            for template in templatelist:
                tempbed.add_field(name=f'Name: {template.name}', value=f"Description: {template.desc}. Category: {template.category}")

            await ctx.send(embed=tempbed)
            return
        tlist = [p.name for p in paradelist]
        if param.capitalize() not in tlist:
            await ctx.send("Sorry The template you requested does not seem to have anything to do with Isaiah's Parade")
            return

        temp = await self.getTemplate(param)
        await ctx.send(temp)

    @commands.command()
    async def example(self, ctx):
        await ctx.send("It was requested and therefore it will be granted. Here is an example")
        await ctx.send(">>>create creature")
        await ctx.send("```Ok, Begin by telling me it's name```")
        await ctx.send("name=Jerry_The_Beast")
        await ctx.send("```Good, now tell me any attributes of Jerry_The_Beast that you want```")
        await ctx.send("age=1004")
        await asyncio.sleep(1)
        await ctx.send("description=very scary")
        await asyncio.sleep(1)
        await ctx.send("something without an equal sign to end")
        await asyncio.sleep(1)
        await ctx.send("```Completed. View with >>>mycreations```")

    @commands.command()
    async def mycreations(self, ctx):
        usercreations = [dic for dic in self.custom_dict_list if dic["userid"] == ctx.author.id]
        if not usercreations:
            await ctx.send("You have not created any items as yet. Get started with >>>help")
            return

        tosend = []
        for creation in usercreations:
            tosend.append(f"Name: {creation['name']}, ID: {creation['itemid']}, Object Type: {creation['objtype']}\n")
        
        p = '\n'.join(tosend)
        await ctx.send(f"""Here is a list of all of your items:
{p}""")
        await ctx.send("You can view more information with >>>view itemid. Using the name will return the first match. Not just yours")

    
    @commands.command()
    async def view(self, ctx, idtoview):
        try:
            idtoview = int(idtoview)
        except ValueError:
            pass

        itemtoview = [x for x in self.custom_dict_list if x["itemid"] == idtoview or x["name"] == idtoview]

        if itemtoview:
            itv = itemtoview[0]
            embed = discord.Embed(
                title="Viewing Object",
                description=f"Showing {itv['username']}'s {itv['objtype']}",
                color=randint(0, 0xffffff)
            )

            for k, v in itv.items():
                if k == "userid":
                    continue
                if k == "guildid": continue
                k = k.capitalize()
                embed.add_field(name=k, value=v)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Could not find any item with that ID")
            return

    @commands.command()
    async def creations(self, ctx):
        itemstoshow = [x for x in self.custom_dict_list if x["guildid"] == ctx.guild.id]
        tosend = []
        for creation in itemstoshow:
            tosend.append(f"Name: {creation['name']}, ID: {creation['itemid']}, Object Type: {creation['objtype']}, Creator: {creation['username']}\n")
        
        p = '\n'.join(tosend)
        await ctx.send("Here is a list of all items created in your server")
        await ctx.send(p)

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
                tochange = await self.bot.wait_for("message", timeout=30, check=check)
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
        try:
            idtodelete = int(idtodelete)
        except ValueError:
            pass

        itemtodelete = [obj for obj in self.custom_dict_list if obj["itemid"] == idtodelete and obj["userid"] == ctx.author.id]

        if itemtodelete:
            itd = itemtodelete[0]
            if not conf:
                await ctx.send(f"This will delete this item permanately. Do >>>delete {idtodelete} True to confirm")
                return

            await ctx.send(f"Deleting {itd['name']}")
            self.custom_dict_list.remove(itd)
            await ctx.send("Successful, for I have devoured it :yum:")
            toupdate = [x for x in self.custom_dict_list if x["itemid"] > itd["itemid"]]
            for changing in toupdate:
                changing["itemid"] = changing["itemid"] - 1
            del itd
        else:
            await ctx.send("I could not find any item belonging to you with that ID")
            return

    
    @commands.command()
    async def actions(self, ctx, idtoget=None):
        if idtoget is None:
            tosend = []
            tosend.append(Item.getcom())
            tosend.append(Person.getcom())
            tosend.append(Creature.getcom())
            tosend.append(Potion.getcom())
            tosend.append(Vehicle.getcom())
            tosend.append(Weapon.getcom())
            tosend.append(Armour.getcom())
            tosend.append(Enemy.getcom())
            tosend.append(Pet.getcom())
            tosend.append(Ability.getcom())
            tosend.append(Passive.getcom())
            tosend.append("All Classes have access to the discard method")
            
            tosend = '\n'.join(tosend)

            await ctx.send(tosend)

        else:
            try:
                itg = int(idtoget)
            except ValueError:
                await ctx.send("That ID is not a number")
                return

            objtoget = [uobj for uobj in self.custom_dict_list if uobj["itemid"] == itg]
            if not objtoget:
                await ctx.send("Could not find an object matching that ID")
                return

            objtoget = objtoget[0]
            uobj = await self.getobj(objtoget)
            await ctx.send(uobj.getcom())

    @commands.command()
    async def do(self, ctx, actionname, objectid):
        try:
            objectid = int(objectid)
        except ValueError:
            await ctx.send("Not a number")
            return
        dicttoobj = [uobj for uobj in self.custom_dict_list if uobj["itemid"] == objectid]
        if not dicttoobj:
            await ctx.send("Could not find an object with that ID")
            return

        toobj = dicttoobj[0]
        print(type(toobj))
        obj = await self.getobj(toobj)

        if actionname.lower() not in obj.getcomlist():
            await ctx.send("That is not a valid action of this object")
            return

        _atd = actionname.lower()
        msg = eval(f"obj.{_atd}()")
        await ctx.send(msg)


    # Functions

    async def getTemplate(self, temptoget):
        if temptoget.lower() in ["item", "potion"]:
            return "name:\ndescription:\ncost:\neffect:\nduration:\ntier:\nhealthup:\npowerup:\nmindmgup:\nmaxdmgup:\ncritup\npotionoritem:"
        elif temptoget.lower() == "weapon":
            return "name:\ndescription:\neffect:\ndamage:\ncritplus:\nlifesteal:\ncost:\ncost:\ntier:"
        elif temptoget.lower() == "armour":
            return "name:\ndescription:\nhealthup:\npowerup:\ncost:\nregen:\nweaponPair:\ntier:\n"
        elif temptoget.lower() in ["passive", "ability"]:
            return "name:\ndescription:\nusagename:\neffect:\npowerX:\npower+:\nhealthup:\nmindmgup:\nmaxdmgup:\ncooldown(onlyforabilities):"
        elif temptoget.lower() == "pet":
            return "name:\ndescription:\ntype:\nnumofstages:\nexptoevolve:\ncurrentstage:\nevolvesinto:\nplaymessage:\nfeedmessage:"
        elif temptoget.lower() == "enemy":
            t = "name:\nhealth:\nmindmg:\nmaxdmg:\nmincoin:\nmaxcoin:\nentrymessage:\nminxp:\ncritchance:\nhealchance:\nability:\npassive:\nattackmsg:\nweapon:\narmour:\nlevel:\n"
            return t

        else:
            return "I'm not quite sure what... but something went wrong"

    async def changekey(self, ctx, otu):
        await ctx.send("Which key would you like to change?")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            try:
                ktc = await self.bot.wait_for("message", timeout=60, check=check)
            except TimeoutError:
                await ctx.send("Took too long... aborting ;p")
                return

            ktc = ktc.content
            if ktc.startswith(">>>"): continue
            if ktc.lower() in self.rwords:
                await ctx.send("You cannot change that key")
                continue

            nktc = [key for key in otu.keys() if key.lower() == ktc.lower()]
            
            if nktc:
                await ctx.send("I have found that key")
                break
            else:
                await ctx.send("I did not find that key. Try again please")
                continue

        await ctx.send("Next...")
        
        while True:
            await ctx.send(f"What would you like to change {nktc} to?")
            try:
                resp = await self.bot.wait_for("message", timeout=60, check=check)
            except TimeoutError:
                await ctx.send("Sigh... Taking a bit too long to answer a relativel simple question... :yawning_face:")
                return
            
            resp = resp.content

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
                ktc = await self.bot.wait_for("message", timeout=60, check=check)
            except TimeoutError:
                await ctx.send("Took too long... aborting ;p")
                return

            ktc = ktc.content
            if ktc.startswith(">>>"): continue

            if ktc.lower() in self.rwords:
                await ctx.send("You cannot change that key")
                continue

            nktc = [key for key in otu.keys() if key.lower() == ktc.lower()]
            
            if nktc:
                await ctx.send("I have found that key")
                break
            else:
                await ctx.send("I did not find that key. Try again please")
                continue

        await ctx.send(f"The value for {nktc[0]} is {otu[nktc[0]]}")
        while True:
            await ctx.send("What would you like to change this value to?")

            try:
                tochange = await self.bot.wait_for("message", timeout=120, check=check)
            except TimeoutError:
                await ctx.send(":yawning_face: Goodbye")
                return

            tc = tochange.content
            if len(tc) > 150:
                await ctx.send("Your value cannot be more than 150 characters")
                continue
            
            break

        otu[nktc[0]] = tc
        await ctx.send("Completed")

    
    async def changepair(self, ctx, otu):
        await self.changekey(ctx, otu)
        await self.changevalue(ctx, otu)           


    async def getuserobj(self, ownerid):
        toreturn = [x for x in self.custom_dict_list if x["userid"] == ownerid]
        
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

        thename = re.findall(r"name=(.+)", msg.content)
        if not thename:
            await ctx.send("Did not get the name. Try again. Format is name=the_name_you_want. For now, I'm leaving. So just run the command again")
            return

        _vname = thename[0]
        _objtomake = objtomake.capitalize()
        _iditem = await self.getid(ctx)
        userobj = classes[_objtomake](True, ctx.author.id, ctx.author.name, _iditem, _objtomake, _vname, ctx.guild.id)
        await self.creating(ctx, userobj)

    async def getid(self, ctx):
        iid = [x["itemid"] for x in self.custom_dict_list]
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
                msg = await self.bot.wait_for("message", timeout=300, check=check)
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
                for creation in attri:
                    key = creation[0]
                    if key.lower() in self.rwords:
                        await ctx.send("You cannot use That as a key because it is a reserved word")
                        continue
                    if " " in key:
                        await ctx.send("Your key must not have in spaces. Use _ or - instead")
                        continue

                    if len(key) > 15:
                        await ctx.send("Your key should not be more than 15 characters")

                    value = creation[1]
                    if len(value) > 150:
                        await ctx.send("Your value cannot be more than 150 characters")

                    setattr(objmaking, key, value)
                    counter += 1
                    if counter >= 20:
                        break
            else:
                await ctx.send("That did not match the key=value format I told you to use 🏋️‍♂️")
                continue

        await ctx.send("Completed. View with >>>mycreations")
        self.custom_dict_list.append(objmaking.__dict__)

    
    async def getobj(self, objtoget):
        _typeobj = objtoget["objtype"]
        p = objtoget
        objtoreturn = classes[_typeobj](p['exists'], p['userid'], p['username'], p['itemid'], p['objtype'], p['name'])
        for k, v in p.items():
            setattr(objtoreturn, k, v)

        return objtoreturn
    

    @tasks.loop(minutes=2)
    async def save(self):
        if len(self.custom_dict_list) > 0:
            with open("customobjects.json", "w") as f:
                json.dump(self.custom_dict_list, f, indent=4)

    # Events

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        etype = type(error)
        trace = error.__traceback__

        # the verbosity is how large of a traceback to make
        # more specifically, it's the amount of levels up the traceback goes from the exception source
        verbosity = 4

        # 'traceback' is the stdlib module, `import traceback`.
        lines = traceback.format_exception(etype, error, trace, verbosity)

        # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
        traceback_text = ''.join(lines)

        # now we can send it to the user
        # it would probably be best to wrap this in a codeblock via e.g. a Paginator
        print(traceback_text)

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

        print(error)


def setup(bot):
    bot.add_cog(objcommands(bot))
