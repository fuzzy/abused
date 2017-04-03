#!/usr/bin/env python

import os
import re
import sys
import copy

if os.path.isfile('./package.use'):
    use = []
    out = {}
    fp = open('./package.use')
    buff = fp.readline()
    while buff:
        if buff[0] != '#':
            use.append(buff.strip())
        buff = fp.readline()
    os.unlink('./package.use')
    # now let's iterate through
    for l in use:
        data = l.split()
        if len(data) > 0:
            while data[0][0] in ('>', '<', '='):
                data[0] = data[0][1:]
            cat = data[0].split('/')[0]
            if cat not in out.keys():
                out[cat] = []
            pkg = re.sub('-[0-9].*', '', data[0].split('/')[1])
            out[cat].append('%s/%s %s' % (cat, pkg, ' '.join(data[1:])))

    os.mkdir('./package.use')
    for l in out.keys():
        fp = open('./package.use/%s' % l, 'w+')
        for v in out[l]:
            fp.write('%s\n' % v)
        fp.close()
