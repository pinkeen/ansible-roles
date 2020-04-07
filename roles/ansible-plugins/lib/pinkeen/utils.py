from pprint import PrettyPrinter

def pprint(obj, **settings):
    if not 'indent' in settings:
        settings['indent'] = 4

    PrettyPrinter(**settings).pprint(obj)

def map_dict(callable, obj, *args):
    return {
        k: callable(v, *args) 
            for k, v in obj.items() 
    }

