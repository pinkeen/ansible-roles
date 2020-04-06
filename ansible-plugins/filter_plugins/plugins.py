from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../lib')))

from pinkeen.ansible.filters import AbstractFilterModule
from pinkeen.ansible.filters.basic import DictFilterModule, ListFilterModule, StringFilterModule
from pinkeen.ansible.filters.docker import DockerFilterModule
from pinkeen.ansible.filters.ini import IniModule

class FilterModule(AbstractFilterModule):
    FILTER_FUNC_PREFIX = 'do_'
    FILTER_BASE_CLASSES = [
        DictFilterModule, 
        ListFilterModule, 
        StringFilterModule,
        DockerFilterModule,
        IniModule
    ]