from jinja2.filters import contextfilter

from pinkeen.utils import map_dict
from pinkeen.ansible.filters import filterclass

@filterclass(strip='do_', prefix='lst_')
class LstFilters(object):

    @staticmethod
    @contextfilter
    def do_list_map(context, lst, filter_name, *args, **kwargs):
        return list(
            map(
                lambda item: context.environment.call_filter(
                    filter_name, item, args, kwargs, context=context
                ),
                lst
            )
        )
