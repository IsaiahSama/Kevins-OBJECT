class TheWorld:

    def __init__(self, exists=False, userid=None, username=None, itemid=None, objtype=None, name=None):
        self.exists = exists
        self.userid = userid
        self.username = username
        self.itemid = itemid
        self.objtype = objtype
        self.name = name

    def getid(self):
        return self.itemid

    def getowner(self):
        return self.itemid


class Item(TheWorld):

    def puton(self):
        return f"Equipped {self.username}'s {self.name}"

    def takeoff(self):
        return f"Took off {self.username}'s {self.name}"

    def drop(self):
        return f"Drops {self.username}'s {self.name}"

class Person(TheWorld):

    def talkto(self):
        return f"Spoke to {self.name}"
    
    def wave(self):
        return f"Waved at {self.name}"

    def stare(self):
        return f"Stares at {self.name}"

class Creature(TheWorld):
    
    def tame(self):
        return f"Managed to tame {self.username}'s {self.name}"

    def runfrom(self):
        return f"Ran from {self.username}'s {self.name}"

    def fight(self):
        return f"Fought {self.username}'s {self.name}"

class Potion(TheWorld):

    def drink(self):
        return f"Gulped down {self.username}'s {self.name}"

    def drop(self):
        return f"Dropped {self.username}'s {self.name}"

class Vehicle(TheWorld):

    def drive(self):
        return f"Drove around in {self.username}'s {self.name}"

    def hit(self):
        return f"hit someone with {self.username}'s {self.name}... Whoops"

class Weapon(TheWorld):

    def swing(self):
        return f"Swings around {self.username}'s {self.name}"

    def strike(self):
        return f"Strikes someone with {self.username}'s {self.name}"

    def showoff(self):
        return f"Shows off {self.username}'s {self.name}"

    def sheathe(self):
        return f"Returns {self.name} to it's sheathe"

class Armour(TheWorld):
    
    def equip(self):
        return F"Equipped {self.username}'s {self.name}"

    def takeoff(self):
        return f"Took off {self.username}'s {self.name}"

    def polish(self):
        return F"Polishes {self.username}'s {self.name}"

class Pet(TheWorld):

    def rub(self):
        return f"Rubs {self.username}'s {self.name}"

    def play(self):
        return f"Plays with {self.username}'s {self.name}"

    def feed(self):
        return f"Feeds {self.username}'s {self.name}"

class Enemy(TheWorld):

    def stare(self):
        return f"Stares at {self.username}'s {self.name}"

    def fight(self):
        return f"Fights {self.username}'s {self.name}"

    def run(self):
        return f"Runs from {self.username}'s {self.name}"

class Ability(TheWorld):

    def use(self):
        return f"Uses {self.username}'s {self.name}"

    def turnon(self):
        return f"Activates {self.username}'s {self.name}"

    def turnoff(self):
        return f"Deactivates {self.username}'s {self.name}"

    def showoff(self):
        return f"Shows off {self.username}'s {self.name}"

class Passive(TheWorld):
    
    def showoff(self):
        return f"Shows off {self.username}'s {self.name}"

    def use(self):
        return f"Is using {self.username}'s {self.name}"
    