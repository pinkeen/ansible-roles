from jinja2.filters import contextfilter

from pinkeen.utils import map_dict
from pinkeen.ansible.filters import filterclass

@filterclass(strip='do_', prefix='obj_')
class ObjFilters(object):
    @staticmethod
    @contextfilter 
    def do_obj_map(context, obj, filter_name, *args, **kwargs):
        return map_dict(
            lambda item: context.environment.call_filter(
                filter_name, item, args, kwargs, context=context
            ),
            obj
        )


    @staticmethod
    @contextfilter
    def do_obj_attr(context, obj, attr, filter_name=None, *args, **kwargs):
        val = obj[attr] if attr in obj else None 

        if filter_name is not None and val is not None:
            val = context.environment.call_filter(
                filter_name, val, args, kwargs, context=context
            )

        return val


    @staticmethod
    def do_obj_keys(obj):
        return obj.keys()


    @staticmethod
    def do_obj_keys_remap(obj={}, keymap={}):
        return { (keymap[key] if key in keymap else key): obj[key] for key in obj }


    @staticmethod
    def do_obj_keys_pick(obj={}, keys=[]):
        return { key: obj[key] for key in keys if key in obj }


    @staticmethod
    def do_obj_keys_reject(obj={}, keys=[]):
        return { key: obj[key] for key in obj if key not in keys }


    @staticmethod
    def do_obj_keys_prefix_with(obj={}, prefix=''):
        return { prefix + key: obj[key] for key in obj }


    @staticmethod
    def do_obj_keys_pick_prefixed(obj={}, prefix=''):
        return dict([(key, obj[key]) for key in obj if key.startswith(prefix)])


    @staticmethod
    def do_obj_to_kv_list(obj={}):
        return [ {k: v} for k, v in obj.items() ]
