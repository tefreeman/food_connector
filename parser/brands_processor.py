from pymongo import collection
import copy
from typing import Dict, List


class BrandsProcessor:
    _brand_names = {}
    is_initialized = False

    def __init__(self, nutritionix_grocery: collection = None):
        if not BrandsProcessor.is_initialized:
            self.collection: collection = nutritionix_grocery
            self._init_brand_names()

    def _init_brand_names(self):
        pos = 0
        for doc in self.collection.find():
            name: str = (doc['name']).lower()
            BrandsProcessor._add_to_brand_name(name, doc['id'])
            if pos > 20:
                break
            pos += 1

    @staticmethod
    def _add_to_brand_name(name: str, brand_id: str):
        if name not in BrandsProcessor._brand_names:
            BrandsProcessor._brand_names[name] = brand_id

    @staticmethod
    def get_brand_names_dict() -> Dict:
        return copy.deepcopy(BrandsProcessor._brand_names)

    def get_brand_items(self, brand_id: str = None, name:str = None):
        if brand_id:
            return self.collection.find_one({'id': brand_id})
        elif name:
            return self.collection.find_one({'name': name})
        else:
            raise Exception("brand_id or name must be defined")