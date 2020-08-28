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

mhelp = MyHelp("Help", "Reveals the help command", ">>>help")

commandlist = MyHelp("Command List", "Shows a list of commands", ">>>commandlist")

cmdlist = [create, template, example, mycreations, view, mhelp, commandlist]
