""" abused.outproc
Provides the OutProc() class, which wraps a PEG parser, and subprocess
pipes.
"""

# Stdlib imports
import re
import subprocess
from typing import Callable, TextIO


class PegParser:

    _callbacks: dict
    _expressions: dict

    def add_trigger(self, patt: str, cbak: Callable) -> bool:
        return False

    def del_trigger(self, id: str) -> bool:
        return False

    def process(self, infp: TextIO) -> None:
        pass


class OutProc:
    pass
