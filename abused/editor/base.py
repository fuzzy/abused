import cmd

# Base class for out editors

class AbusedBase(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

    # Command 'quit' | 'exit' | ctrl+D
    def help_EOF(self):
        print('\n'.join(('Exit the program immediately.',
                         'Aliases: quit, exit, <ctrl>+d',
                         'Example: exit')))
    
    def do_EOF(self, line=None):
        print('')
        return True

    def help_exit(self):
        self.help_EOF()
        
    def do_exit(self, line=None):
        return self.do_EOF()

    def help_quit(self):
        self.help_EOF()
        
    def do_quit(self, line=None):
        return self.do_EOF()

