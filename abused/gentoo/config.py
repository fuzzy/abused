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

    def _read_config(self, fpath=False):
        retv = []
        if fpath and os.path.isfile(fpath):
            with open(fpath) as fp:
                buff = fp.readline()
                while buff:
                    retv.append(buff.strip().split())
            return retv
        return False

    def _write_config(self, fpath=False, cdata=()):
        if fpath and os.path.isfile(fpath) and len(cdata) >= 1:
            with open(cfgfile, "w+") as fp:
                for line in cdata:
                    fp.write(f"{' '.join(line)}\n")

    def config_exists(self, atom=False):
        if atom:
            cat, pkg = atom.split("/")
            cfgfile = f"{self._base_dir}/{cat}"
            cfgdata = self._read_config(cfgfile)

            for line in cfgdata:
                if line[0].find(pkg) != -1:
                    return True

        return False

    def update_config(self, atom=False, *args):
        if atom:
            cat, pkg = atom.split("/")
            cfgfile = f"{self._base_dir}/{cat}"
            outdata = []
            cfgfp = open(cfgfile, "r")
            buff = cfgfp.readline()

            while buff:
                if buff.strip().split()[0].find(atom) != -1:
                    outdata.append(f"{atom} {' '.join(args)}")
                else:
                    outdata.append(buff.strip())
                buff = cfgfp.readline()

            cfgfp.close()
            cfgfp = open(cfgfile, "w+")

            for line in outdata:
                cfgfp.write(f"{' '.join(line)}\n")

            cfgfp.close()

            return True
        return False


class PackageUse(GentooConfig):
    def __init__(self, ptype=False):
        GentooConfig.__init__(self, ptype)
