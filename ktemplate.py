class tempdesc:
    def __init__(self, name, desc, category=None):
        self.name = name
        self.desc = desc
        self.category = category

    def istemplate(self):
        if self.category is None:
            return False
        return True

item = tempdesc("Item", "Any Item", "<>Battle")
person = tempdesc("Person", "Create your own person >:)")
creature = tempdesc("Creature", "OwO what's this, your own creature? :o")
potion = tempdesc("Potion", "Mhm yes, potions", "<>Battle")
vehicle = tempdesc("Vehicle", "Any vehicle you can think of... Make it")
weapon = tempdesc("Weapon", "Seems Familiar 🤔", "<>Battle")
armour = tempdesc("Armour", "A weapon, without armour... pfft", "<>Battle")
pet = tempdesc("Pet", "It's so nicee... probably", "<>Social")
enemy = tempdesc("Enemy", "This seems... very specific", "<>Battle")
ability = tempdesc("Ability", "Your very own ability... YES", "<>Battle")
passive = tempdesc("Passive", "Perfect for complimenting your ability", "<>Battle")


templatelist = [creature, person, vehicle, item, potion, weapon, armour, pet, enemy, ability, passive]
paradelist = [temp for temp in templatelist if temp.istemplate()]
