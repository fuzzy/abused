#!/usr/bin/env python2

import os
import re
import cmd
import sys
import shlex
import string
import subprocess


from abused.scale       import *
from abused.editor.main import *


def usage():
    print('Usage: %s <args> or %s [emerge options and package names]' % (
        os.path.basename(sys.argv[0]),
        os.path.basename(sys.argv[0])))
    print('\n'.join(('Args:',
                     '--help | -h   \t\tShow this help.',
                     '--use-sync <f>\t\tSync use flags from <f> to /etc/portage/package.use',
                     '              \t\t(This generally is only used internally.)')))
    sys.exit(1)

if __name__ == '__main__':
    if sys.argv[1] == '--use-sync':
        inLines = []
        print('this is not done yet')
        try:
            if os.path.isfile(sys.argv[2]):
                print('Reading: %s' % sys.argv[2])
                ifp = open(sys.argv[2])
                buff = ifp.readline()
                while buff:
                    inLines.append(buff.strip())
                    buff = ifp.readline()
                ifp.close()
            else:
                print('%s: File (%s) does not exist.' % (
                    Scale('ERROR').bold().red(),
                    sys.argv[2]))
                sys.exit(-1)
        except IndexError:
            print("Not to mention you didn't even do it right.")

        for l in inLines:
            cat = l.split()[0].split('/')[0]
            ouf = '/etc/portage/package.use/%s' % cat

            # read in the output content, if any
            outLines = []
            if os.path.isfile(ouf):
                ifp = open(ouf)
                buf = ifp.readline()
                while buf:
                    outLines.append(buf.strip())
                    buf = ifp.readline()
                ifp.close()

            # find the line (if any) that matches the new one and remove it
            for ol in range(0, len(outLines)):
                print(outLines[ol])
                print(l)
                if outLines[ol].split()[0] == l.split()[0]:
                    outLines.pop(ol)

            # Now add out line to the outfiles, and sync it to disk
            outLines.append(l)
            print('write -> %s' % ouf)
            for l in outLines:
                print(l)
            
            
    elif sys.argv[1] in ('--help', '-h'):
        usage()
    else:
        try:
            app = Abused()
        except KeyboardInterrupt:
            # TODO KILL THE FUCKING PROC IF IT'S LIVE
            sys.exit(1)
