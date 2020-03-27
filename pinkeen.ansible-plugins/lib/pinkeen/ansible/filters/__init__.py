import inspect
import types

from pinkeen.utils import pprint

def filterclass(strip='do_', prefix=''):
    FUNC_ATTR = '__filter_name'

    def decorate(cls):

        def get_filters():
            functions = inspect.getmembers(cls,
                lambda member: 
                    inspect.isfunction(member) 
                    or inspect.ismethod(member)
            )

            for n, f in functions:
                pprint(f.__dict__)

            filters = {
                function.__dict__[FUNC_ATTR] if FUNC_ATTR in function.__dict__ else name: function 
                    for name, function in functions
            }

            filters = {
                prefix + name[len(strip):]: function 
                    for name, function in filters.items()
                        if name.startswith(strip)
            }

            return filters
            
        filters = get_filters()

        for name, function in filters.items():
            function.__dict__[FUNC_ATTR] = name

        cls.filters = lambda self: filters

        return cls

    return decorate

    
    