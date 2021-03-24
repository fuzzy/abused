""" abused.emerge  """

# Stdlib imports
import os
import re
import sys
import shlex
import string
import subprocess
from typing import Callable, TextIO

# Internal imports
from abused.config import *
from abused.package import *


class Emerge:
    def __init__(self):
        self._cfg = read_config()

    def _noop(self):
        pass

    def _doop(self):
        pass

    def _cmd(self):
        pass
