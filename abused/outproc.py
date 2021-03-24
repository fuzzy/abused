""" abused.outproc
Provides the OutProc() class, which wraps a PEG parser, and subprocess
pipes.
"""

# Stdlib imports
import re
import subprocess
from typing import Callable, TextIO


class PegParser:
    """ abused.outproc.PegParser """

    _callbacks: dict
    _expressions: dict

    def add_trigger(self, id: str, patt: str, cbak: Callable) -> bool:
        """ PegParser.add_trigger(id: str, patt: str, cbak: Callable) -> bool """
        try:
            self._expressions[id] = re.compile(patt)
            self._callbacks[id] = cbak
            return True
        except:
            return False

    def del_trigger(self, id: str) -> bool:
        """ PegParser.del_trigger(self, id: str) -> bool """
        try:
            self._expressions.pop(id)
            self._callbacks.pop(id)
            return True
        except KeyError:
            return False

    def process(self, infp: TextIO) -> None:
        """ PegParser.process(self, infp: TextIO) -> None """
        try:
            buff = infp.readline()
            while buff:
                buff = infp.readline()
        except AttributeError:
            return


class OutProc:
    pass
