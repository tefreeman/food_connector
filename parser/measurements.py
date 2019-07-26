from helpers import open_file_as_json, save_json_to_file
from typing import Dict, Set
from pint import UnitRegistry
from enum import Enum
from collections import namedtuple

Extra_Measurements =  namedtuple('_extra_m', ['sci', 'obj', 'mod'])


class MType(Enum):
    sci = 0
    obj = 1
    mod = 2
    none = 3


class Measurements:
    _ureg = UnitRegistry()
    _extra_m = Extra_Measurements({}, set(), set())

    @staticmethod
    def _load_measurements():
        M = Measurements
        j_dict = open_file_as_json('measurements.json')
        for obj in j_dict['sci'].items():
            M._extra_m.sci[obj[0]] = obj[1]

        for obj in j_dict['obj']:
            M._extra_m.obj.add(obj)

        for obj in j_dict['mod']:
            M._extra_m.mod.add(obj)

    @staticmethod
    def add_measurement_type(m_obj: str, m_key: str, obj_name=""):
        M = Measurements
        if m_key == 'sci':
            if obj_name not in M._extra_m.sci:
                M._extra_m.sci[obj_name] = m_obj
        elif m_key == 'obj':
            M._extra_m.obj.add(m_obj)
        elif m_key == 'mod':
            M._extra_m.mod.add(m_obj)
        else:
            print('Error measurement key is not in _keys set')
            return
        M._save_new_change()

    @staticmethod
    def _save_new_change():
        M = Measurements
        json = {'sci': M._extra_m.sci, 'obj': list(M._extra_m.obj), 'mod': list(M._extra_m.mod)}
        save_json_to_file('measurements.json', json)

    @staticmethod
    def get_measurement_type(stemmed_word: str):
        M = Measurements
        if stemmed_word in M._extra_m.sci:
            try:
                m_type = Measurements._ureg.parse_expression(stemmed_word)
                return True, m_type
            except:
                print("Could not parse ", stemmed_word, " as a sci measurement ")
        elif stemmed_word in M._extra_m.obj:
            return True, 'obj'
        elif stemmed_word in M._extra_m.mod:
            return True, 'mod'
        else:
            return False, None
