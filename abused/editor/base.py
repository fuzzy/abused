import cmd

# Base class for out editors

class AbusedBase(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

    # Command 'quit' | 'exit' | ctrl+D
    def help_exit(self):
        print('\n'.join(('Exit the program immediately.',
                         'Aliases: quit, exit, <ctrl>+d',
                         'Example: exit')))
    
    def do_EOF(self, line=None):
        print('')
        return True
        
    def do_exit(self, line=None):
        return self.do_EOF()

    def do_quit(self, line=None):
        return self.do_EOF()

