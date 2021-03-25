""" abused.outproc
Provides the PortageParser() class, which wraps a PEG parser, and subprocess
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
    """ abused.outproc.PortageParser() """

    _cfg: AbusedConfig = read_config()
    _peg: PegParser = PegParser()

    def __init__(self) -> None:
        # patterns for parsing package lines
        self._peg.add_trigger(
            "package",
            "^\[.*\] [a-zA-Z0-9\-]*/[a-zA-Z0-9\-\_\]*-([0-9][0-9a-zA-Z\-\_]*)$",
            self.parse_package,
        )
        # self._init_keyword()
        # self._init_license()
        # self._init_env()
        # self._init_mask()

    def _cmd(self, noop: bool = True) -> str:
        retv: list[str] = []
        # Determine if we need to do privilege escalation
        if os.getenv("USER").lower() != "root":
            retv.append(self._cfg.emerge.su_tool)
        # Seed the rest of our command
        for prep_line in (
            "env",
            "EMERGE_DEFAULT_OPTS=''",
            f"MAKEOPTS='{self._cfg.emerge.makeopts}'",
            "emerge",
        ):
            retv.append(prep_line)
        # Determine if this should be a No-OP
        if noop:
            for arg in self._cfg.emerge.noop:
                retv.append(arg)
        # And seed in the portage arguments as configured
        for arg in self._cfg.emerge.default_opts:
            retv.append(arg)
        # And we are done!
        return " ".join(retv)

    def parse_package(self, line: str) -> None:
        """ PortageParser.parse_package(line: str) -> None """
        pass
