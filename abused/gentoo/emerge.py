# Stdlib imports
import os
import re


class Portage:

    _config = "/etc/portage/make.conf"

    def __init__(self):
        self._opts = {}

        if os.path.isfile(self._config):
            with open(self._config) as fp:
                buff = fp.readline()
                while buff:
                    if (
                        len(buff.strip()) >= 1
                        and buff.strip()[0] != "#"
                        and buff.find("=") != -1
                    ):
                        val = None
                        key, vtmp = re.split("=", buff.strip(), maxsplit=1)
                        if vtmp[0] in ('"', "'"):
                            val = vtmp[1:-1]
                        else:
                            val = vtmp
                        self._opts[key] = val
                    buff = fp.readline()

        tarch = os.uname().machine
        if tarch == "x86_64":
            self._arch = "amd64"
        elif tarch == "aarch64":
            self._arch = "arm64"

    @property
    def arch(self):
        return self._arch
