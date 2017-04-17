
import os


from abused.scale       import *
from abused.squish      import *
from abused.editor.base import *


# This is the package editor

class AbusedPkg(AbusedBase):

    prompt = Scale(':: ').bold().cyan()

    def __init__(self, pkg={}):
        AbusedBase.__init__(self)
        
        if pkg == {}:
            print('%s: Not a valid package object' % Scale('ERROR').bold().red())
            return
        
        for t in ('category', 'package', 'version', 'variables'):
            if t not in pkg.keys():
                print('%s: Not a valid package object' % Scale('ERROR').bold().red())
                return
            
        try:
            if len(pkg['variables'].keys()) == 0:
                print('%s: This package (%s/%s) has no variables to edit.' % (
                    Scale('INFO').bold().cyan(),
                    pkg['category'],
                    pkg['package']))
        except TypeError:
            print('%s: Not a valid package object' % Scale('ERROR').bold().red())
            return

        self.pkg     = pkg
        self.keys    = pkg['variables'].keys()
        self.editing = ''
        self.edited  = False
        
        self.keys.sort()
        self._updatePrompt()
        self.do_refresh()

    def edit(self):
        self.cmdloop()
        if self.edited:
            return squish(self.pkg)
        else:
            return self.pkg

    def _updatePrompt(self):
        pend        = Scale('::').bold().cyan()
        self.prompt = '%s %s ' % (Scale(self.editing).bold().green(), pend)

    #####
    # These are general behaviour methods
    #####
    
    def default(self, line):
        return self.do_edit(line)

    #####
    # These are the command implementations
    #####

    def do_edit(self, line):
        var = self.pkg['variables'][self.editing]
        for ln in line.strip().split():
            for f in range(0, len(var)):
                test = False
                # our flag with no modifier
                if ln[0] == '-':
                    home = ln[1:]
                else:
                    home = ln
                # the existing flag with no modifier
                if var[f][0] == '-':
                    away = var[f][1:]
                else:
                    away = var[f]

                # Determine if we even need to worry
                if home == away:
                    # First this way:
                    if var[f].find(ln.strip()) != -1:
                        test = var[f]
                        # and then this way:
                    elif ln.strip().find(var[f]) != -1:
                        test = var[f]

                    if test:
                        self.edited = True
                        if ln[0] == '-' and var[f][0] != '-':
                            var[f] = ln
                        elif ln[0] != '-' and var[f][0] == '-':
                            var[f] = ln
        self.do_refresh()
        
    # Command: var
    # Argument: index or name of variable
    # Example: var 1 or var USE
    def help_var(self):
        print('\n'.join(('',
                         'Command: var <arg>',
                         'Argument: Index # or name of variable',
                         'Example A: var 1',
                         'Example B: var USE',
                         '',
                         'Change the variable being edited.',
                         '')))

    def do_var(self, line):
        if line.isdigit() and int(line) < len(self.keys):
            self.editing = self.keys[int(line)]
        else:
            if line in self.keys:
                self.editing = line
        self._updatePrompt()
        self.do_refresh()

    # Command: refresh
    # Argument: None        os.system('clear')
    def help_refresh(self):
        print('\n'.join(('',
                         'Command: refresh',
                         'Example: refresh',
                         '',
                         'Redraw the screen it helps keep things tidy.',
                         '')))
        
    def do_refresh(self, line=None):
        os.system('clear')
        if 'USE' in self.keys and self.editing == '':
            self.editing = 'USE'
        elif len(self.keys) > 0 and self.editing == '':
            self.editing = self.keys[0]
        self._updatePrompt()
        print('\n%s:' % Scale('Last known state').green())
        print(self.pkg['line'])
        if len(self.keys) > 0:
            print('\n%s:' % Scale('Available variables to edit').green())
            for k in range(0, len(self.keys)):
                print('%s: %s' % (Scale(k).bold().red(), Scale(self.keys[k]).bold().yellow()))
            print('\n%s:\n%s\n' % (
                Scale('Current %s values' % self.editing).green(),
                ' '.join(self.pkg['variables'][self.editing])))
        
