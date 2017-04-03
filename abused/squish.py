
def squish(pkg=False):
    try:
        use = []
        for k in pkg['variables'].keys():
            for f in pkg['variables'][k]:
                if f[0] not in ('(', '{'):
                    if f[0] == '-' and k.lower() == 'use':
                        use.append(f)
                    elif f[0] != '-':
                        if k.lower() == 'use':
                            use.append(f)
                        else:
                            use.append('%s_%s' % (k.lower(), f))
        pkg['flattened'] = use
        return pkg
    except KeyError:
        pass

