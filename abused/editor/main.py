
import copy
import time

from abused.scale          import *
from abused.emerge         import *
from abused.editor.base    import *
from abused.editor.package import *

# This is the main abused interface

class Abused(AbusedBase):

    # our command parser object
    emerge = Emerge()
    # Cmd stuff
    prompt = Scale('>> ').bold().green()
    
    def __init__(self):
        AbusedBase.__init__(self)
        self.emerge.noop()
        self.cmdloop()

    #####
    # These are general behaviour methods
    #####

    def default(self, line=None):
        try:
            if line.find('/') != -1:
                self.do_edit(line)
        except AttributeError:
            pass
        
    # Command 'edit'
    # Argument string (ex: net-ftp/ncftp)
    def help_edit(self):
        print('\n'.join(('',
                         'Command: edit <category/package> <...>',
                         'Argument: string (ie: net-ftp/ncftp)',
                         '',
                         'This command will allow you to edit the build variables',
                         'for the package specified. It must be one that is in the',
                         'list above.',
                         '')))
        
    def do_edit(self, line):
        for o in line.split():
            if o.find('/') != -1:
                data = o.split('/')
                for p in self.emerge.packages:
                    if p['category'] == data[0] and p['package'].find(data[1]) != -1:
                        o = AbusedPkg(p)
                        p = o.edit()
        self.do_refresh()

    # Command 'refresh'
    # Argument: none
    def help_refresh(self):
        print('\n'.join(('',
                         'Command: refresh',
                         'Argument: None',
                         '',
                         'Use this to refresh the view of the package list from the last run.',
                         '')))

    def do_refresh(self, line=None):
        os.system('clear')
        for i in self.emerge.replay:
            print(i)
