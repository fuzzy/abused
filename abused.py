#!/usr/bin/env python2

import os
import re
import cmd
import sys
import shlex
import string
import subprocess

Flags = {}

def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

class Scale(str):
    def __len__(self):
        '''
        This ensures that you will always get the actual length of the string,
        minus the extended characters. Which is of course important, when you
        are calculating output field sizes. Requires the re module.
        '''
        tmp = self[:]
        cnt = 0
        for i in re.sub('\\x1b[\[0-9;]*m', '', tmp):
            cnt += 1
        return(cnt)

    def __getattr__(self, method):
        '''
        This is essentially an implimentation of Ruby's .method_missing
        that shortens the code dramatically, and allows for simply extending
        to support other escape codes. As a note, the modifier methods like
        .bold() and .underline() and such, need to come before the color
        methods. The color should always be the last modifier.
        '''
        method_map = {
            'black':     {'color': True,  'value': 30, 'mode': 'm'},
            'red':       {'color': True,  'value': 31, 'mode': 'm'},
            'green':     {'color': True,  'value': 32, 'mode': 'm'},
            'yellow':    {'color': True,  'value': 33, 'mode': 'm'},
            'blue':      {'color': True,  'value': 34, 'mode': 'm'},
            'purple':    {'color': True,  'value': 35, 'mode': 'm'},
            'cyan':      {'color': True,  'value': 36, 'mode': 'm'},
            'white':     {'color': True,  'value': 37, 'mode': 'm'},
            'clean':     {'color': False, 'value': 0,  'mode': 'm'},
            'bold':      {'color': False, 'value': 1,  'mode': 'm'},
            'underline': {'color': False, 'value': 4,  'mode': 'm'},
            'blink':     {'color': False, 'value': 5,  'mode': 'm'},
            'reverse':   {'color': False, 'value': 7,  'mode': 'm'},
            'conceal':   {'color': False, 'value': 8,  'mode': 'm'},
        }

        def get(self, **kwargs):
            if method_map[method]['color']:
                reset='[0m'
            else:
                reset=''

            return(
                Scale('%s[%s%s%s%s' % (
                    reset,
                    method_map[method]['value'],
                    method_map[method]['mode'],
                    self,
                    reset
                )
            ))

        if method in method_map:
            return get.__get__(self)
        else:
            raise(AttributeError, method)

class Pkg(object):

    def __str__(self):
        if supports_color():
            if self._type == 'binary':
                pkgname = Scale('%s/%s-%s' % (
                    self._category, self._pkgname, self._pkgvers)).purple()
            else:
                pkgname = Scale('%s/%s-%s' % (
                    self._category, self._pkgname, self._pkgvers)).green()
        else:
            pkgname = '%s/%s-%s' % (
                self._category, self._pkgname, self._pkgvers)

        fl = []
        for op in self._op:
            if op in ('R', '~'):
                fl.append(Scale(op).bold().yellow())
            elif op in ('U'):
                fl.append(Scale(op).bold().cyan())
            elif op in ('*'):
                fl.append(Scale(op).red())
            elif op in ('N'):
                fl.append(Scale(op).bold().green())
            else:
                fl.append(op)
        while len(fl) < 5:
            fl.insert(0, ' ')
            
        retv = '[%5s] %s' % (''.join(fl), pkgname)

        if self._prevers != None:
            retv += ' [%s]' % Scale(self._prevers).blue()
            
        for a in self._flags.keys():
            retv += ' %s="' % a
            for b in self._flags[a]:
                try:
                    retv += '%s ' % str(b)
                except TypeError:
                    pass
            tretv = '%s"' % retv[:-1]
            retv  = tretv

        return retv

    def __repr__(self):
        return self.__str__()
            
    def __init__(self, data):
        self._flags                = {}
        self._op                   = []
        upgrade                    = False
        self._prevers              = None
        for idx in range(0, len(data)):
            try:
                if data[idx] == '[' and not upgrade:
                    self._type     = data[idx+1]
                    t_idx          = 2
                    while data[idx+t_idx] != ']':
                        self._op.append(data[idx+t_idx])
                        t_idx += 1
                elif data[idx] == ']' and not upgrade:
                    tdata          = ''.join(data[idx+1:]).split('/')
                    self._category = tdata[0]
                    self._pkgname  = tdata[1].split('-')[0]
                    self._pkgvers  = tdata[1].split('%s-' % self._pkgname)[1].split('::')[0]
                    upgrade        = True
                elif data[idx] == '[' and upgrade:
                    t_idx          = idx+1
                    while data[t_idx] != ']':
                        t_idx += 1
                    self._prevers  = ''.join(data[idx+1:t_idx]).split('::')[0]
                elif data[idx+1] == '=':
                    if data[idx] not in self._flags.keys():
                        self._flags[data[idx]] = []
                    if data[idx] not in Flags.keys():
                        Flags[data[idx]] = []
                        
                    if data[idx] == 'USE':
                        t_i        = True
                    else:
                        t_i        = False
                        
                    for f in data[idx+2][1:-1].split():
                        self._flags[data[idx]].append(Flag(f, iterative=t_i))
                        Flags[data[idx]].append(Flag(f, iterative=t_i))
                        
            except IndexError:
                pass

    def binary(self):
        if self._type == 'binary':
            return True
        else:
            return False

class Flag(object):

    _state = True
    _new   = ''
    _trans = ''
    _force = False
    _bound = False

    def __sanitize(self, mobj):
        if mobj.group(0) in ('*', '%', '(', ')', '{', '{', '-'):
            return ''
        else:
            return mobj.group(0)
            
    def __init__(self, flag, iterative=False):
        self._iterative = iterative
        # Is this flag forced?
        if flag[0] == '(':
            self._force = True
            tflag = flag[1:-1]
            flag = tflag
        # Is this flag bound to FEATURES settings?
        if flag[0] == '{':
            self._bound = True
            tflag = flag[1:-1]
            flag = tflag
        # Is this flag disabled?
        if flag[0] == '-':
            self._state = False
            tflag = flag[1:]
            flag  = tflag
        # Is this flag a new one?
        if flag[-1:] == '%':
            self._new = '%'
            tflag = flag[:-1]
            flag  = tflag
        # Is this flag in transition?
        if flag[-1:] == '*':
            self._trans = '*'
            tflag = flag[:-1]
            flag  = tflag

        self._name = flag
                    
    def __str__(self):
        # inner helper function
        def dump(s='', b='', a=''):
            if self._trans == '*':
                return '%s%s%s%s%s' % (b, Scale(s).green(), self._new, self._trans, a)
            elif self._new == '%':
                return '%s%s%s%s%s' % (b, Scale(s).yellow(), self._new, self._trans, a)
            elif self._state:
                return '%s%s%s%s%s' % (b, Scale(s).red(), self._new, self._trans, a)
            else:
                return '%s%s%s%s%s' % (b, Scale(s).blue(), self._new, self._trans, a)
            
        if not self._iterative and self._state:
            if self._bound:
                if self._state: return dump(self._name, '{', '}')
                else: return dump('-%s' % self._name, '{', '}')
            elif self._force:
                if self._state: return dump(self._name, '(', ')')
                else: return dump('-%s' % self._name, '(', ')')
            else:
                if self._state: return dump(self._name)
                else: return dump('-%s' % self._name)
        else:
            if self._bound:
                if self._state: return dump(self._name, '{', '}')
                else: return dump('-%s' % self._name, '{', '}')
            elif self._force:
                if self._state: return dump(self._name, '(', ')')
                else: return dump('-%s' % self._name, '(', ')')
            else:
                if self._state: return dump(self._name)
                else: return dump('-%s' % self._name)

    def enabled(self):
        return self._state
    
class EmergeOp(cmd.Cmd):
    
    _emergeOpts = {
        'fireDrill': '-pvbkuD --color n --binpkg-respect-use=y',
        'liveFire':  '-vbkuD --quiet-build --color n --binpkg-respect-use=y',
    }
    _cmdLine    = sys.argv[1:]
    _data       = {
        'optTarget': 'fireDrill',
        'pkgLines':  [],
        'pkgs':      [],
        'vnames':    []
    }

    # Cmd stuff
    prompt = Scale('>> ').bold().green()

    def _sanitize(self, data):
        retv = ''
        if data.find('\x1b') != -1:
            tmp = filter(lambda x: x in string.printable, data)
            retv += re.sub('(\{|\})', '', re.sub('\[[0-9\;]+m', '', tmp))
            return retv
        return data
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self._emerge(sys.argv[1:])
        # Now lets record our flags
        self.keys = Flags.keys()
        # and set our default to USE
        self._default = False
        for i in range(0, len(self.keys)):
            if self.keys[i] == 'USE':
                self._default = i
                self.prompt = '%s %s ' % (
                    Scale(self.keys[i]).bold().cyan(),
                    Scale('>>').bold().green())
        if not self._default:
            self._default = 0
            self.prompt = '%s %s ' % (
                    Scale(self.keys[0]).bold().cyan(),
                    Scale('>>').bold().green())
        self._promptPrep()
        # and fire off the commandloop
        self.cmdloop()

    def _emerge(self, args):
        global Flags
        os.system('clear')
        self._data['pkgs'] = []
        print("Please wait while the emerge operation is examined.\n")
        # start off the cmd string
        cmd = 'env EMERGE_DEFAULT_OPTS="%s"' % self._emergeOpts[self._data['optTarget']]
        # Add any flags we have recorded
        for f in Flags.keys():
            cmd += ' %s="' % f
            st = []
            for p in (0, 1):
                for t in Flags[f]:
                    if p == 0 and t.enabled():
                        st.append(str(t))
                    elif p == 1 and not t.enabled():
                        st.append(str(t))
            cmd += ' '.join(st)
            cmd += '"'
        # And finalize the command string
        cmd += ' emerge %s' % ' '.join(args)
        Flags = {}
        print('DEBUG: %s' % self._sanitize(cmd))
        cmd_p = subprocess.Popen(
            self._sanitize(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable="/bin/bash"
        )
        buff = cmd_p.stdout.readline()
        while buff:
            data = list(shlex.shlex(buff.strip()))
            if len(data) > 0:
                if data[0] == '[':
                    self._data['pkgs'].append(Pkg(data))
            buff = cmd_p.stdout.readline()

    def _promptPrep(self):
        for i in self._data['pkgs']:
            #if not i.binary():
            print(i)
        print('')
        print('''
You can edit any of the following variables with the command: var N

Typing in a flag by it'self with or without the '-' modifier, will be
merged into the current list, and once you are satisfied, you can retry
with your edits by typing 'retry' or simply hitting <ENTER> on an empty
line.

More information can be found through the help command.
''')
        for k in range(0, len(self.keys)):
            print('%3d# %s' % (k, self.keys[k]))
        print('')
            
    # Command 'quit' | 'exit' | ctrl+D
    def help_EOF(self):
        print('\n'.join(('Exit the program immediately.',
                         'Aliases: quit, exit, <ctrl>+d',
                         'Example: exit')))
    
    def do_EOF(self, line):
        print('')
        return True

    def help_exit(self):
        self.help_EOF()
        
    def do_exit(self, line):
        return self.do_EOF()

    def help_quit(self):
        self.help_EOF()
        
    def do_quit(self, line):
        return self.do_EOF()

    # flag entry
    def default(self, line):
        for tkn in line.strip().split():
            enabled = True
            # remove any pre-existing '-' modifier
            if tkn[0] == '-':
                enabled = False
                d = tkn[1:]
            else:
                d = tkn
            # Go through the existing flags and see if we can find this one
            for etkn in Flags[self.keys[self._default]]:
                if etkn._name == d:
                    if enabled and not etkn.enabled():
                        etkn._state = True
                    if not enabled and etkn.enabled():
                        etkn._state = False

    # Command 'refresh'
    def help_refresh(self):
        print('\n'.join(('refresh',
                         'Clear the screen and reprint the package data.')))

    def do_refresh(self, line):
        os.system('clear')
        self._promptPrep()
        
    # Command 'retry'
    def help_retry(self):
        print('\n'.join(('retry',
                         'Retry the emerge operation with your changes.')))

    def do_retry(self, line):
        self._emerge(sys.argv[1:])
        self._promptPrep()

    # Command 'commit'
    def help_commit(self):
        print('\n'.join(('commit',
                         'Commit your changes by running the emerge operation for real.',
                         'This works by pressing <ENTER> on an empty line as well.')))
    def do_commit(self, line):
        self._data['optTarget'] = 'liveFire'
        self._emerge(sys.argv[1:])
    
    def emptyline(self):
        self.do_commit(None)
        
    # Command 'var'
    def help_var(self):
        print('\n'.join(('var [index]',
                         'Switch editing mode to the variable referenced by "index"',
                         'Example: var 2')))
        
    def do_var(self, index):
        if int(index) < len(self.keys):
            self._default = int(index)
            self.prompt = '%s %s ' % (
                Scale(self.keys[self._default]).bold().cyan(),
                Scale('>>').bold().green())
        else:
            print('%s: There are only %d keys.' % (
                Scale('error').bold().red(), len(self.keys)))

if __name__ == '__main__':
    try:
        app = EmergeOp()
    except KeyboardInterrupt:
        sys.exit(1)
