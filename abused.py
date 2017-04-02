#!/usr/bin/env python2

import os
import re
import cmd
import sys
import shlex
import string
import subprocess

# DEBUG
from pprint import pprint

from abused.editor.main import *
    

if __name__ == '__main__':
    try:
        app = Abused()
        #app = EmergeOp()
    except KeyboardInterrupt:
        sys.exit(1)
