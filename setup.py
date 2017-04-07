#!/usr/bin/env python2

from distutils.core import setup

setup(
    name='abused',
    version='0.1.3',
    description='A Basic USE eDitor is an inline use flag editor for Gentoo Linux.',
    author="Mike 'Fuzzy' Partin",
    author_email='fuzzy@fumanchu.org',
    url='https://git.thwap.org/fuzzy/abused',
    packages=['abused', 'abused.editor'],
    scripts=['bin/abused', 'bin/abused_usefix'],
)
