import re

classes = {}
def register(klass):
    classes[klass.__name__] = klass
    return klass
    
class TheWorld:

    def __init__(self, exists=False, userid=None, username=None, itemid=None, objtype=None, name=None, guildid=None):
        self.exists = exists
        self.userid = userid
        self.username = username
        self.itemid = itemid
        self.objtype = objtype
        self.name = name
        self.guildid = guildid

    def getid(self):
        return self.itemid

    def getowner(self):
        return self.itemid

    def discard(self):
        return f"Discarded away {self.username}'s {self.name}"

@register
class Item(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Items are puton, takeoff and drop"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.strip("and")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg


    def puton(self):
        return f"Equipped {self.username}'s {self.name}"

    def takeoff(self):
        return f"Took off {self.username}'s {self.name}"

    def drop(self):
        return f"Drops {self.username}'s {self.name}"

@register
class Person(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Person class are talkto, wave and stare"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.strip("and")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg


    def talkto(self):
        return f"Spoke to {self.name}"
    
    def wave(self):
        return f"Waved at {self.name}"

    def stare(self):
        return f"Stares at {self.name}"

@register
class Creature(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Creatures are tame, runfrom, runto and fight"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.strip("and")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg


    def tame(self):
        return f"Managed to tame {self.username}'s {self.name}"

    def runfrom(self):
        return f"Ran from {self.username}'s {self.name}"

    def runto(self):
        return f"Ran towards {self.username}'s {self.name}"

    def fight(self):
        return f"Fought {self.username}'s {self.name}"

@register
class Potion(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Potions are drink and drop"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.split("and")
        return lmsg


    def drink(self):
        return f"Gulped down {self.username}'s {self.name}"

    def drop(self):
        return f"Dropped {self.username}'s {self.name}"

@register
class Vehicle(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Vehicles are drive, hit and crash"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.replace(" and ", ",")
        lmsg = lmsg.replace(" ", "")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg

    def drive(self):
        return f"Drove around in {self.username}'s {self.name}"

    def hit(self):
        return f"hit someone with {self.username}'s {self.name}... Whoops"

    def crash(self):
        return f"Crashed {self.username}'s {self.name}"

@register
class Weapon(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Weapons are swing, strike, showoff and sheathe"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.replace(" and ", ",")
        lmsg = lmsg.replace(" ", "")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg


    def swing(self):
        return f"Swings around {self.username}'s {self.name}"

    def strike(self):
        return f"Strikes someone with {self.username}'s {self.name}"

    def showoff(self):
        return f"Shows off {self.username}'s {self.name}"

    def sheathe(self):
        return f"Returns {self.name} to it's sheathe"

@register
class Armour(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Armour are equip, takeoff and polish"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.replace(" and ", ",")
        lmsg = lmsg.replace(" ", "")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg


    def equip(self):
        return F"Equipped {self.username}'s {self.name}"

    def takeoff(self):
        return f"Took off {self.username}'s {self.name}"

    def polish(self):
        return F"Polishes {self.username}'s {self.name}"

@register
class Pet(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Pets are rub, play and feed"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.replace(" and ", ",")
        lmsg = lmsg.replace(" ", "")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg


    def rub(self):
        return f"Rubs {self.username}'s {self.name}"

    def play(self):
        return f"Plays with {self.username}'s {self.name}"

    def feed(self):
        return f"Feeds {self.username}'s {self.name}"

@register
class Enemy(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Enemies are stare, fight and run"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.replace(" and ", ",")
        lmsg = lmsg.replace(" ", "")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg


    def stare(self):
        return f"Stares at {self.username}'s {self.name}"

    def fight(self):
        return f"Fights {self.username}'s {self.name}"

    def run(self):
        return f"Runs from {self.username}'s {self.name}"

@register
class Ability(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Abilities are use, turnon, turnoff and showoff"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.replace(" and ", ",")
        lmsg = lmsg.replace(" ", "")
        nlmsg = lmsg.split(",")
        for content in nlmsg:
            if "," in content:
                content = content.strip(",")
        return nlmsg


    def use(self):
        return f"Uses {self.username}'s {self.name}"

    def turnon(self):
        return f"Activates {self.username}'s {self.name}"

    def turnoff(self):
        return f"Deactivates {self.username}'s {self.name}"

    def showoff(self):
        return f"Shows off {self.username}'s {self.name}"

@register
class Passive(TheWorld):

    @classmethod
    def getcom(self):
        return "Actions for Passives are showoff and use"

    @classmethod
    def getcomlist(self):
        msg = self.getcom()
        lmsg = re.findall(r"are\s(.+)", msg)
        lmsg = lmsg[0]
        lmsg = lmsg.split("and")
        return lmsg


    def showoff(self):
        return f"Shows off {self.username}'s {self.name}"

    def use(self):
        return f"Is using {self.username}'s {self.name}"
    