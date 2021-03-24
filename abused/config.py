""" abused.config """

# Stdlib imports
import os
import types
from typing import Any, Union

# 3rd party imports
import yaml


VALID_KEYS = Union[str, int, float]


class AbusedConfig(dict):
    """abused.config.AbusedConfig({})
    This is a custom dictionary object that allows items to be
    referenced as attributes, and generally just makes things
    a little bit nicer.

    Example:
    >>> from abused.config import AbusedConfig
    >>> obj = AbusedConfig()
    >>> obj.foo = "bar"
    >>> print(obj)
    {'foo': 'bar'}
    >>> print(obj.foo)
    bar
    >>>
    """

    def __init__(self, data: dict = {}) -> None:
        dict.__init__(self, {})
        for k, v in data.items():
            if type(v) != dict:
                self[k] = v
            else:
                self[k] = AbusedConfig(v)

    def __getattr__(self, attr: str) -> Any:
        if attr in self.keys():
            return dict.__getitem__(self, attr)
        return dict.__getattribute__(self, attr)

    def __setattr__(self, attr: VALID_KEYS, value: Any) -> None:
        dict.__setitem__(self, attr, value)


def merge_config(
    odata: Union[AbusedConfig, dict], ndata: Union[AbusedConfig, dict]
) -> AbusedConfig:
    """merge_config(AbusedConfig, AbusedConfig) -> AbusedConfig
    Merge down the second instance into the first. If a key exists, it's
    value will be overwritten. New keys, will be added.
    """
    return odata


def read_config() -> AbusedConfig:
    """read_config() -> AbusedConfig
    This will look for /etc/abused.cfg, /etc/abused/abused.cfg,
    and ~/.abusedrc, in that order, and merge them into the running
    configuration.
    """
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
