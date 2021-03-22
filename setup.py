#!/usr/bin/env python2

# Stdlib
import os

from distutils.core import setup


# Internal
from abused.scale import *


# Output flags
info = Scale(">>>").green()
warn = Scale("!!!").bold().yellow()
error = Scale("!!").bold().red()

# Determine if we have sudo, which will be required for non-root operations
# Absense is not fatal, but it's use is encouraged.
have_sudo = False
for p in os.getenv("PATH").split(":"):
    try:
        if "sudo" in os.listdir(p):
            have_sudo = True
            break
    except OSError:
        pass
if not have_sudo:
    print("%s You do not have sudo installed." % warn)
    print("%s It's presence is not mandatory, but is encouraged." % warn)
else:
    print("%s Sudo installed: %s" % (info, Scale("True").bold().green()))

# Determine if we have pyyaml installed
try:
    import yaml

    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper
    print("%s PyYAML installed: %s" % (info, Scale("True").bold().green()))
    # cfg = yaml.load(open('./abused.cfg'), Loader=Loader)
except ImportError:
    print("%s You do not have PyYAML installed." % error)
    print("%s You can install it with the following command:" % error)
    print("%s pip install -r requirements.txt" % error)
    # system('%spip install -r requirements.txt')
    # import yaml
    sys.exit(1)

print("%s Installing...\n" % info)
# Do the big final dance
setup(
    name="abused",
    version="0.3.6",
    description="A Basic USE eDitor is an inline use flag editor for Gentoo Linux.",
    author="Mike 'Fuzzy' Partin",
    author_email="fuzzy@fumanchu.org",
    url="https://git.thwap.org/fuzzy/abused",
    packages=["abused", "abused.editor"],
    scripts=["bin/abused", "bin/abused_usefix"],
)

existing_config = False
for i in ("/etc/abused/abused.cfg", "%s/.abusedrc" % os.getenv("HOME")):
    if os.path.exists(i):
        existing_config = True

if not existing_config:
    print(
        "\n%s You should copy the abused.cfg to either /etc/abused/abused.cfg," % info
    )
    print("%s ${HOME}/.abusedrc, or always run abused from this diretory.\n" % info)
else:
    print(
        "\n%s Pre-existing installation detected. Please review the abused.cfg," % info
    )
    print("%s in the source distribution and see if any changes are needed in" % info)
    print("%s your configuration files." % info)
