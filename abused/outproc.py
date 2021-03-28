""" abused.outproc
Provides the PortageParser() class, which wraps a PEG parser, and subprocess
pipes.
"""

# Stdlib imports
import re
import shlex
import string
import subprocess
from typing import Callable, TextIO

# Internal imports
from abused.config import *


class PortagePackage:
    category: str
    package: str
    version: str
    variables: dict
    line: str
    flattened: list


class PortageParser:
    """ abused.outproc.PortageParser() """

    _cfg: AbusedConfig = read_config()

    def __init__(self) -> None:
        pass

    def _sanitize(self, data):
        retv = ""
        if data.find("\x1b") != -1:
            tmp = filter(lambda x: x in string.printable, data)
            retv += re.sub("(\{|\}|\*|\%)", "", re.sub("\[[0-9\;]+m", "", tmp))
            return retv
        return data

    def _portage_cmd(self, noop: bool = True) -> str:
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

    def _cmdproc(self, parse: bool = True) -> None:
        self._replay: list = []
        self._packages: list = []
        os.system("clear")

        if parse:
            cmd_p = subprocess.Popen(
                self._sanitize(self._portage_cmd()),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                executable="/bin/bash",
            )
            buff = cmd_p.stdout.readline()
            while buff:
                data = buff.decode("utf-8").strip()
                self._parser(data)
                print(data)
                self._replay.append(data)
                buff = cmd_p.stdout.readline()
        else:
            os.system(self._sanitize(self._portage_cmd(noop=False)))

    def _parser(self, data: str) -> None:
        ldata = list(shlex.shlex(self._sanitize(data)))
        if len(ldata) > 0 and ldata[0] == "[":
            pkg = PortagePackage()
            lmax = len(data)
            for tkn in range(0, lmax):
                pass
