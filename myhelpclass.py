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
 "My main command. You must also tell what it is you wish to create. Select one from >>>template",
 ">>>create templatename")

template = MyHelp("Template", "Used to view a list of available templates for object creation available",
">>>template")

example = MyHelp("Example", "Shows an example of using the >>>create command", ">>>example")

mycreations = MyHelp("My Creations", "Reveals all of your Creations", ">>>mycreations")

cmdlist = [create, template, example, mycreations]
