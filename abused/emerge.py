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


class PegParser:

    _callbacks: dict
    _expressions: dict

    def add_trigger(self, patt: str, cbak: Callable) -> bool:
        return False

    def del_trigger(self, id: str) -> bool:
        return False

    def process(self, infp: TextIO) -> None:
        pass


class EmergeParser:
    def __init__(self):
        pass


class Emerge:
    def __init__(self):
        self._cfg = read_config()

    def _noop(self):
        pass

    def _doop(self):
        pass

    def _cmd(self):
        pass
