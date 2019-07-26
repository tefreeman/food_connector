import sys
from numbers import Number
from collections import Set, Mapping, deque
from typing import Dict, List
from bson.json_util import dumps, loads
zero_depth_bases = (str, bytes, Number, range, bytearray)
iteritems = 'items'


def getsize(obj_0):
    """Recursively iterate to sum size of object & members."""
    _seen_ids = set()

    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, zero_depth_bases):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)


def sort_key_number_dict(d: Dict, descending: bool) -> List[Dict]:
    dict_list = list(d.items())
    dict_list.sort(key=lambda x: x[1], reverse=descending)
    return dict_list


def save_json_to_file(name: str, d: [Dict, List]):
    with open(name, 'w') as outfile:
        outfile.write(dumps(d))


def open_file_as_text(name: str) -> str:
    with open(name, 'r') as readfile:
        return readfile.read()


def open_file_as_json(name: str) -> Dict:
    with open(name, 'r') as readfile:
        return loads(readfile.read())
