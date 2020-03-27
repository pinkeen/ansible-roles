from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../lib')))

from pinkeen.utils import pprint
from pinkeen.ansible.filters import filterclass
from pinkeen.ansible.filters.obj import ObjFilters
from pinkeen.ansible.filters.lst import LstFilters

@filterclass()
class FilterModule(ObjFilters, LstFilters):
    pass

print('--- COMBINED ---')
m = FilterModule()
pprint(m.filters())