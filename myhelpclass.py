class MyHelp:
    def __init__(self, name, desc, usage):
        self.name = name
        self.desc = desc
        self.usage = usage

    def returnhelp(self):
        msg = f"""Name: {self.name}
Description: {self.desc}
How to use: {self.usage}"""

        return msg

create = MyHelp("Create",
 "My main command. You must also tell what it is you wish to create. Select one from >>>template. Use >>>help",
 ">>>create")

template = MyHelp("Template", "Used to view a list of available templates for object creation available",
">>>template")

example = MyHelp("Example", "Shows an example of using the >>>create command", ">>>example")

mycreations = MyHelp("My Creations", "Reveals all of your Creations", ">>>mycreations")

view = MyHelp("View", "Tells you everything about the item whose id you enter", ">>>view itemid")

delete = MyHelp("Delete", "Deletes an object belonging to you that matches the ID you say", ">>>delete itemid")

mhelp = MyHelp("Help", "Reveals the help command", ">>>help")

update = MyHelp("Update", "Allows you to update one of your items", ">>>update itemid")

commandlist = MyHelp("Command List", "Shows a list of commands", ">>>commandlist")

mobject = MyHelp("OBJECT", "Shows what the acronym OBJECT in Kevin's OBJECT stands for", ">>>OBJECT")

action = MyHelp("Actions", "Shows the actions available for an object. Note these are class specific", ">>>actions [id]")

do = MyHelp("Do", "Does an action available to the class of the object whose id you specify", ">>>do nameofaction objectid")

cmdlist = [create, template, example, mycreations, view, delete, mhelp, commandlist, mobject, action, do, update]
