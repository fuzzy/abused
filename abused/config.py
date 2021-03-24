""" abused.config """

# Stdlib imports
import os
import types
from typing import Any, Union

# 3rd party imports
import yaml


ValidKeys = Union[str, int, float]
ValidCfgs = Union[AbusedConfig, dict]


class AbusedConfig(dict):
    def __init__(self, data: dict = {}) -> None:
        dict.__init__(self, self._recurse_data(data))

    def _recurse_data(self, data: dict) -> dict:
        retv = AbusedConfig()
        for k, v in data.items():
            if type(v) != dict:
                retv[k] = v
            else:
                retv[k] = AbusedConfig(v)
        return retv

    def __getattr__(self, attr: string) -> Any:
        if attr in self.keys():
            return dict.__getitem__(self, attr)
        return dict.__getattribute__(self, attr)

    def __setattr__(self, attr: ValidKeys, value: Any) -> None:
        dict.__setitem__(self, attr, value)


def merge_config(odata: ValidCfgs, ndata: ValidCfgs) -> AbusedConfig:
    return AbusedConfig()


def read_config() -> AbusedConfig:
    retv = AbusedConfig()
    for fn in (
        "/etc/abused.cfg",
        "/etc/abused/abused.cfg",
        f'{os.getenv("HOME")}/.abusedrc',
    ):
        if os.path.isfile(fn):
            data = AbusedConfig(yaml.safe_load(open(fn).read()))
            retv = merge_config(retv, AbusedConfig(yaml.safe_load))

    return retv
