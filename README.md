# Abused (A basic USE editor)

Abused is an inline USE flag editor for Gentoo Linux. It handles edits to build
variables (like LINGUAS, PYTHON_TARGETS, etc) interactively, and persists them
to /etc/portage/package.use/ files named for the category the package is in.
(ie: /etc/portage/package.use/dev-libs, /etc/portage/package.use/app-shells,
etc). Abused is immune to almost any changes made to portage as it doesn't parse
or try to recreate the work that portage does, it simply parses emerge output
and manages files in /etc/portage/. Non root users will not need to call abused
via sudo, as it will automatically use sudo if it is not being run as root. Sudo
is a requirement for this as no other mechanism is supported.

## Installation

```
git clone https://git.thwap.org/fuzzy/abused
cd abused && sudo ./setup.py install
```

![usage](/abused.gif)
