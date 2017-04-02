import os
import re
import sys
import shlex
import string
import subprocess


class Emerge(object):
    __eOpts   = {
        'noop': '-p',                 # pretend
        'args': [
            '-v',                     # verbose
            '-b',                     # make binpkg
            '-k',                     # use binpkg if available
            '-u',                     # update
            '-D',                     # deep
            '--color=y',              # Show color output if possible
            '--newuse',               # reinstall/rebuild if use flags differ
            '--autounmask-write=n',   # do not automatically unmask packages
            '--keep-going=y',         # restart emerge after package build failure if possible
        ],
    }

    # a "package" is a dict object, with the following structure:
    # { 'category':  string,
    #   'package':   string,
    #   'version':   string,
    #   'variables': { 'FLAG_NAME': [string, string], ... }}
    packages  = []
    replay    = []

    def __init__(self):
        if os.getenv('USER').lower() != 'root':
            self.sudo = 'sudo'
        else:
            self.sudo = ''

    def _sanitize(self, data):
        retv = ''
        if data.find('\x1b') != -1:
            tmp = filter(lambda x: x in string.printable, data)
            retv += re.sub('(\{|\}|\*|\%)', '', re.sub('\[[0-9\;]+m', '', tmp))
            return retv
        return data
            
    def _parser(self, data=None):
        ldata = list(shlex.shlex(self._sanitize(data)))
        if len(ldata) > 0 and ldata[0] == '[':
            cat = {'category':  None,
                   'package':   None,
                   'version':   None,
                   'variable':  None}
                   
            pkg = {'category':  '',
                   'package':   '',
                   'version':   '',
                   'variables': {},
                   'line':      data}

            #print(ldata)
            lmax = len(ldata)
            for tkn in range(0, lmax):
                # ']' signals the end of the operation type symbols and the start
                # of the 'version' part of the package
                if ldata[tkn] == ']':
                    cat['category'] = False
                # Now we know that up until the '/' character we will be looking at
                # the category name
                elif cat['category'] == False and ldata[tkn] != '/':
                    pkg['category'] += ldata[tkn]
                elif cat['category'] == False and ldata[tkn] == '/':
                    cat['category'] = True
                    cat['package'] = False
                # Coming after the '/' character is the package name
                elif cat['package'] == False and not re.match('-[0-9]', ''.join(ldata[tkn:tkn+2])):
                    pkg['package'] += ldata[tkn]
                elif cat['package'] == False and re.match('-[0-9]', ''.join(ldata[tkn:tkn+2])):
                    cat['package'] = True
                    cat['version'] = False
                # The general boundary for the package name / package version is a 2
                # character string matching '-[0-9]'
                elif cat['version'] == False and ldata[tkn] != ':':
                    pkg['version'] += ldata[tkn]
                elif cat['version'] == False and ldata[tkn] == ':':
                    cat['version'] = True
                # after the ':' character we start looking for build variables
                if tkn < lmax-1:
                    if ldata[tkn+1] == '=':
                        cat['variable'] = ldata[tkn]
                        if ldata[tkn] not in pkg['variables'].keys():
                            pkg['variables'][ldata[tkn]] = []
                    elif ldata[tkn-1] == '=':
                        for f in ldata[tkn][1:-1].split():
                            pkg['variables'][cat['variable']].append(f)
                        cat['variable'] = None
                    
            self.packages.append(pkg)
        pass

    def _cmd(self, cmd):
        self.replay = []
        os.system('clear')
        print('DEBUG: %s' % cmd.strip())
        
        cmd_p = subprocess.Popen(
            self._sanitize(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable="/bin/bash"
        )
        buff = cmd_p.stdout.readline()
        while buff:
            self._parser(buff.strip())
            print(buff.strip())
            self.replay.append(buff.strip())
            buff = cmd_p.stdout.readline()
            
            
    def noop(self):
        cmd = '%s emerge %s %s %s' % (self.sudo,       
                                      self.__eOpts['noop'],
                                      ' '.join(self.__eOpts['args']),
                                      ' '.join(sys.argv[1:]))
        self._cmd(cmd)
        return
        
    def run(self):
        cmd = '%s emerge %s FOO' % (self.sudo,
                                    ' '.join(self.__eOpts['args']))
        self._cmd(cmd)
        return
