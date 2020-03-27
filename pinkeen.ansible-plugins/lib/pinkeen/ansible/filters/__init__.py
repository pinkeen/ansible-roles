import inspect
import types

from pinkeen.utils import pprint

class AbstractFilterModule(object):
    FILTER_NAME_PREFIX = ''
    FILTER_FUNC_PREFIX = ''
    FILTER_FUNC_STRIP_PREFIX = True
    FILTER_BASE_MAP = {}
    FILTER_BASE_CLASSES = []

    def create_filter_name(self, func_name):
        if self.FILTER_FUNC_STRIP_PREFIX and func_name.startswith(self.FILTER_FUNC_PREFIX):
            filter_name = func_name[len(self.FILTER_FUNC_PREFIX):]
        else:
            filter_name = func_name
        
        return self.FILTER_NAME_PREFIX + filter_name

    def create_base_filter_map(self):
        filters = self.FILTER_BASE_MAP
        
        for cls in self.FILTER_BASE_CLASSES:
            obj = cls()
            if hasattr(obj, 'filters'):
                filters.update(getattr(obj, 'filters')())

        return filters


    def create_own_filter_map(self):
        funcs = inspect.getmembers(self.__class__,
            lambda member: 
                inspect.isfunction(member) 
                or inspect.ismethod(member)
        )

        return {
            self.create_filter_name(func_name): func
                for func_name, func in funcs
                    if func_name.startswith(self.FILTER_FUNC_PREFIX)
        }


    def filters(self):
        filters = self.create_base_filter_map()
        filters.update(self.create_own_filter_map())
        
        return filters
    
    
    