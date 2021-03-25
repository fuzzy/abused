""" abused.outproc
Provides the OutProc() class, which wraps a PEG parser, and subprocess
pipes.
"""

# Stdlib imports
import re
import subprocess
from typing import Callable, TextIO

# Internal imports
from abused.config import *


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
                data = buff.strip()
                for k, v in self._expressions.items():
                    if v.match(buff):
                        self._callbacks[k](buff)
                buff = infp.readline()
        except AttributeError:
            return


class PortageParser:

    _cfg: AbusedConfig = read_config()
    _peg: PegParser = PegParser()

    def __init__(self) -> None:
        self._init_package()
        self._init_keyword()
        self._init_license()
        self._init_env()
        self._init_mask()

    def _cmd(self, noop: bool = True) -> str:
        retv = [
            "env",
            "EMERGE_DEFAULT_OPTS=''",
            f"MAKEOPTS='{self._cfg.emerge.makeopts}'",
            "emerge",
        ]

        if noop:
            for arg in self._cfg.emerge.noop:
                retv.append(arg)
        for arg in self._cfg.emerge.default_opts:
            retv.append(arg)

        return " ".join(retv)

    def _init_package(self) -> None:
        pass

    def _init_keyword(self) -> None:
        pass

    def _init_license(self) -> None:
        pass

    def _init_env(self) -> None:
        pass

    def _init_mask(self) -> None:
        pass
