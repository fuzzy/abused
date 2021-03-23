""" abused.gentoo.config """

# Stdlib imports
import os
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

    _base_dir = "/home/fuzzy/gentoo/package."
    _pkg_type = False

    def __init__(self, ptype=False):
        if ptype:
            try:
                self._pkg_type = GentooConfigTypes(ptype).value
                self._base_dir = f"{self._base_dir}{self._pkg_type}"
                print(self._base_dir)
            except ValueError:
                ab_fatal(
                    "Something very wrong has happened in GentooConfig.__init__().",
                    ptype,
                )

    def _read_config(self, fpath=False):
        retv = []
        try:
            with open(fpath) as fp:
                buff = fp.readline()
                while buff:
                    if buff[0] != "#":
                        retv.append(buff.strip().split())
                    buff = fp.readline()
        except FileNotFoundError:
            pass
        return retv

    def _write_config(self, fpath=False, cdata=()):
        dpath = os.path.dirname(fpath)

        if not os.path.isdir(dpath):
            os.makedirs(dpath)

        if fpath and len(cdata) >= 1:
            with open(fpath, "bw+") as fp:
                for line in cdata:
                    fp.write(f"{line}\n".encode("utf-8"))
            return True

        return False

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
            tmpdata = self._read_config(cfgfile)
            outdata = [
                "# This file is managed by abused",
            ]

            if len(tmpdata) >= 1:
                for line in tmpdata:
                    if line[0].find(atom) != -1:
                        outdata.append(f"{atom} {' '.join(args)}")
                    else:
                        outdata.append(line)
            else:
                outdata.append(f"{atom} {' '.join(args)}")

            return self._write_config(cfgfile, outdata)
        return False


class PackageUse(GentooConfig):
    def __init__(self):
        GentooConfig.__init__(self, ptype="use")


class PackageLicense(GentooConfig):
    def __init__(self):
        GentooConfig.__init__(self, "license")


class PackageEnv(GentooConfig):
    def __init__(self):
        GentooConfig.__init__(self, "env")


class PackageMask(GentooConfig):
    def __init__(self):
        GentooConfig.__init__(self, "mask")


class PackageKeywords(GentooConfig):
    def __init__(self):
        GentooConfig.__init__(self, "accept_keywords")
