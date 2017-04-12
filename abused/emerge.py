# Stdlib
import os
import re
import sys
import shlex
import string
import subprocess


# 3rd party
import yaml


# internal
from abused.scale  import *
from abused.squish import squish


class Emerge(object):
    
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
        self.config = self._getConfig()
    
    def _getConfig(self):
        for p in ('/etc/abused/', '%s/.' % os.getenv('HOME'), './'):
            if os.path.isfile('%sabused.cfg' % p):
                return yaml.load(open('%sabused.cfg' % p))
        return {}

    def _getOpts(self, noop=True):
        if noop:
            start = self.config['emerge']['default_opts']['noop']
        else:
            start = []
        return start + self.config['emerge']['default_opts']['op']
        
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
                   'line':      data,
                   'flattened': []}

            #print(ldata)
            lmax = len(ldata)
            for tkn in range(0, lmax):
                # ']' signals the end of the operation type symbols and the start
                # of the 'version' part of the package
                if ldata[tkn] == ']' and cat['category'] == None:
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
                            if f[0] not in ('(', '{'):
                                pkg['variables'][cat['variable']].append(f)
                        cat['variable'] = None
                    
            self.packages.append(pkg)
        pass

    def _cmd(self, cmd):
        self.replay   = []
        self.packages = []
        os.system('clear')
        print('%s %s' % (Scale('>>').green(), cmd))
        
        cmd_p = subprocess.Popen(
            self._sanitize('env EMERGE_DEFAULT_OPTS="" %s' % cmd),
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
        cmd = '%s emerge %s %s' % (self.sudo,
                                   ' '.join(self._getOpts(noop=True)),
                                   ' '.join(sys.argv[1:]))
        self._cmd(cmd)
        return
        
    def doop(self):
        cmd = '%s emerge %s %s' % (self.sudo,
                                   ' '.join(self._getOpts(noop=False)),
                                   ' '.join(sys.argv[1:]))
        os.system('clear')
        os.system(cmd)
        sys.exit(0)
