
# Stdlib

import os
import types


# 3rd party

import yaml


class AbusedConfig(dict):
    '''
This is a simple sublcass of the dict object that allows keys to be
referenced as attributes.
    '''
    def __getattr__(self, attr):
        if attr in self.keys():
            return self.__getitem__(attr)
        else:
            raise KeyError, attr

    def __setattr__(self, attr, val):
        self.__setitem__(attr, val)

def descend(data={}):
    data = AbusedConfig(data)
    for k in data.keys():
        if type(data[k]) in (types.ListType, types.TupleType):
            for i in range(0, len(data[k])):
                if type(data[k][i]) == types.DictType:
                    data[k][i] = descend(data[k][i])
        elif type(data[k]) == types.DictType:
            # convert the current item to an AbusedConfig() object
            data[k] = AbusedConfig(descend(data[k]))
    return data
        
def OpenConfig():
    '''
Returns an AbusedConfig() object containing a dictionary resulting from the load
of one of the available locations of the config. If no config is found, OSError
is raised
    '''    
    # Hunt for the config and load it if found
    rdata = False
    for i in ('%s/.abusedrc' % os.getenv('HOME'), '/etc/abused/abused.cfg'):
        if os.path.exists(i):
            rdata = descend(yaml.load(open(i)))
            if os.getenv('USER').lower() != 'root':
                rdata.emerge.sudo = 'sudo '
            else:
                rdata.emerge.sudo = ''
            return rdata
    # fail if not
    if not rdata:
        raise OSError, 'No config file found.'
