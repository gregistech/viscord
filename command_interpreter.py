class CommandInterpreter(object):
    def interpret(self, text):
        com, *args = text.split()
        return (com[1:], args)

