# Stdlib imports
from enum import Enum

# Internal imports
from abused.output import *


class GentooConfigTypes(Enum):
    USE = "use"
    LICENSE = "license"
    MASK = "mask"
    ENV = "env"
    ACCEPT_KEYWORDS = "accept_keywords"


class GentooConfig:

    _base_dir = "/etc/gentoo/package."
    _pkg_type = False
    _format = False

    def __init__(self, ptype=False):
        if ptype:
            try:
                self._pkg_type = GentooConfigTypes(ptype).value
                if os.path.isdir(f"{self._base_dir}{self._pkg_type}"):
                    self._base_dir = f"{self._base_dir}{self._pkg_type}"
            except ValueError:
                ab_fatal(
                    "Something very wrong has happened in GentooConfig.__init__().",
                    ptype,
                )


class PackageUse(GentooConfig):
    def __init__(self, ptype=False, pformat=False):
        GentooConfig.__init__(self, ptype)

    def config_exists(self, atom=False):
        if atom:
            cat, pkg = atom.split("/")
            cfgfile = f"{self._base_dir}/{cat}"

            if os.path.isfile(f"{cfgfile}"):
                with open(cfgfile, "r") as fp:
                    buff = fp.readline()
                    while buff:
                        if buff.strip().split()[0].find(pkg) != -1:
                            return True
                        buff = fp.readline()
                    fp.close()
                    return False
