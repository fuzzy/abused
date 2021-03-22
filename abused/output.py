# Stdlib imports
import sys

# 3rd party imports
from blessings import Terminal

term = Terminal()
prompt = ">>"


def ab_info(msg, **kwargs):
    print(f"{term.bold_green(prompt)} {msg}")
    for k, v in kwargs.items():
        print(f"{term.bold_cyan(prompt)}   {k} = {v}")


def ab_warn(msg, **kwargs):
    print(f"{term.bold_yellow(prompt)} {msg}")
    for k, v in kwargs.items():
        print(f"{term.bold_cyan(prompt)}   {k} = {v}")


def ab_debug(msg, **kwargs):
    print(f"{term.bold_cyan(prompt)} {msg}")
    for k, v in kwargs.items():
        print(f"{term.bold_cyan(prompt)}   {k} = {v}")


def ab_error(msg, **kwargs):
    print(f"{term.bold_red(prompt)} {msg}")
    for k, v in kwargs.items():
        print(f"{term.bold_cyan(prompt)}   {k} = {v}")


def ab_fatal(msg, **kwargs):
    ab_error(msg, **kwargs)
    sys.exit(1)
