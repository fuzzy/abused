
# Stdlib imports
from enum import Enum

# Internal imports
from abused.output import *


class GentooConfigTypes(Enum):
    USE = 'use'
    LICENSE = 'license'
    MASK = 'mask'
    ENV = 'env'
    ACCEPT_KEYWORDS = 'accept_keywords'


class GentooConfig:

    _base_dir = '/etc/gentoo/package.'
    _pkg_type = False

    def __init__(self, ptype=False):
        if ptype:
            try:
                self._pkg_type = GentooConfigTypes(ptype).value
            except ValueError:
                ab_fatal('Something very wrong has happened in GentooConfig.__init__().', ptype)
