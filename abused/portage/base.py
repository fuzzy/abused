
# Stdlib

import os


# Internal

from abused.config import *
from abused.scale  import *

# Logic

class PortageBase(object):
    '''
Class: PortageBase
Author: Mike 'Fuzzy' Partin
    '''

    _base   = '/etc/portage'
    _config = OpenConfig()
    _mTypes = ('single', 'split')
        
    def __init__(self, pType=False):
        if not pType or pType not in self._config.abused.persist.keys():
            print(pType)
            raise ValueError, 'You must pass a valid type to the PortageBase constructor'
        else:
            try:
                if self._config.abused.persist[pType].style in self._mTypes:
                    self._mType  = self._config.abused.persist[pType].style
                else:
                    raise ValueError, 'Value of abused->%s->style in your abused config, is invalid' % pType
            except KeyError, AttributeError:
                raise ValueError, 'Value of abused->%s->style in your abused config, is invalid' % pType
            self._pType          = pType
            if pType == 'keywords':
                self._baseTarget = '%s/package.accept_%s' % (self._base, pType)
            else:
                self._baseTarget = '%s/package.%s' % (self._base, pType)

    def __collect(self):
        # We absolutely do not care what the setting for this target is in the config
        # this is because we collect it into an array regardless of it's format. If
        # the format is changing from what it is now, then the _sync() method will
        # handle all of that. We also strip all comments. I would like to potentially
        # look at reworking the file/dir sync stuff to include a generic parser that
        # gives some *doc like functionality for the comments, to apply metadata to an
        # entry. Seems like a worthwhile idea.
        lines = []
        # is it a split file target?
        if os.path.isdir(self._baseTarget):
            for i in os.listdir(self._baseTarget):
                fp = open('%s/%s' % (self._baseTarget, i))
                buff = fp.readline()
                while buff:
                    if len(buff.strip()) > 0:
                        if buff.strip()[0] != '#':
                            lines.append(self.__strip(buff.strip()))
                    buff = fp.readline()
                fp.close()
        # and if it's a single file target
        elif os.path.isfile(self._baseTarget):
            fp = open(self._baseTarget)
            buff = fp.readline()
            while buff:
                if buff.strip()[0] != '#':
                    lines.append(self.__strip(buff.strip()))
                buff = fp.readline()
            fp.close()
        # this may trigger for symlinks we shall see
        else:
            return lines
        # and finally hand things off
        return lines

    def __clean(self):
        # We don't care what format things are in currently because we're going to blow
        # it completely away
        print('%s Removing %s' % (Scale('>>>').green(), self._baseTarget))
        os.system('%srm -rf %s' % (self._config.emerge.sudo, self._baseTarget))
        if self._mType == 'single':
            print('%s Creating file: %s' % (Scale('>>>').green(), self._baseTarget))
            os.system('%stouch %s' % (self._config.emerge.sudo, self._baseTarget))
        else:
            print('%s Creating directory: %s' % (Scale('>>>').green(), self._baseTarget))
            os.system('%smkdir -p %s' % (self._config.emerge.sudo, self._baseTarget))

    def __strip(self, line=None):
        td = line.strip().split()
        # trim off any atom prefix operators
        while td[0][0] in ('<', '>', '=', '!', '~', '*'):
            td[0] = '%s' % td[0][1:]
        # then trim off the version if any
        tn = '%s' % td[0]
        td[0] = '%s' % re.sub('-[0-9][0-9\.\-a-zA-Z]*', '', tn)
        return ' '.join(td)
            
    def __sync(self, data=[]):
        if len(data) > 0 and self._mType == 'single':
            try:
                print('%s Syncing %s' % (Scale('>>>').green(), self._baseTarget))
                fp = open(self._baseTarget, 'w+')
                data.sort()
                for i in data:
                    fp.write('%s\n' % i)
                fp.close()
            except IOError:
                print('%s Permission denied: %s' % (Scale('!!!').bold().red(),
                                                    self._baseTarget))
                sys.exit(1)
        elif len(data) > 0 and self._mType == 'split':
            sdata = {}
            data.sort()
            for itm in data:
                pf = itm.split()[0].split('/')[0]
                if pf not in sdata.keys():
                    sdata[pf] = []
                sdata[pf].append(itm)
            for fk in sdata.keys():
                print('%s Syncing %s/%s' % (Scale('>>>').green(), self._baseTarget, fk))
                try:
                    fp = open('%s/%s' % (self._baseTarget, fk), 'w+')
                    for ln in sdata[fk]:
                        fp.write('%s\n' % ln)
                    fp.close()
                except IOError:
                    print('%s Permission denied: %s/%s' % (Scale('!!!').bold().red(),
                                                           self._baseTarget, fk))
                    
    def resync(self):
        lines = self.__collect()
        self.__clean()
        self.__sync(lines)
        
