from helpers import sort_key_number_dict
from typing import Dict, List
from language_tools import LanguageTools
from ingredient import IngredientTuple


class CombinedProperties:
    _brand_names = {}
    _serving_units = {}
    _measurement_none_count = 0
    _brand_none_count = 0

    @staticmethod
    def add_ingredient(doc: IngredientTuple):
        if doc.serving_unit is not None:
            CombinedProperties._add_measurement(doc.serving_unit)
        else:
            CombinedProperties._measurement_none_count += 1

        if doc.measures is not None:
            for measure in doc.measures:
                if measure['measure'] is not None:
                    CombinedProperties._add_measurement(measure['measure'])
                else:
                    CombinedProperties._measurement_none_count += 1

        if doc.brand_name is not None:
            CombinedProperties._add_brand_name(doc.brand_name)
        else:
            CombinedProperties._brand_none_count += 1

    @staticmethod
    def _add_brand_name(text: str):
        text = text.lower()
        if text not in CombinedProperties._brand_names:
            CombinedProperties._brand_names[text] = 0
        CombinedProperties._brand_names[text] += 1

    @staticmethod
    def _add_measurement(text: str):
        text = text.lower()
        if text not in CombinedProperties._serving_units:
            CombinedProperties._serving_units[text] = 0
        CombinedProperties._serving_units[text] += 1

    @staticmethod
    def is_brand(text: str):
        if text in CombinedProperties._brand_names:
            return True
        else:
            return False

    @staticmethod
    def is_measurement(text: str):
        if text in CombinedProperties._serving_units:
            return True

    @staticmethod
    def get_sorted_properties(descending=True):
        brands = sort_key_number_dict(CombinedProperties._brand_names, descending=descending)
        serving_units = sort_key_number_dict(CombinedProperties._serving_units, descending=descending)
        return brands, serving_units

