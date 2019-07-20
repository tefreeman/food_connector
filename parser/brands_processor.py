from pymongo import collection
import copy
from typing import Dict, List
from ingredients_processor import IngredientsProcessor
from database import Database
from config import Config


class BrandsProcessor:
    _brand_names = {}
    is_initialized = False

    def __init__(self):
        if not BrandsProcessor.is_initialized:
            self.collection: collection = Database.get_collection(Config().nutritionix_db_name, Config().grocery_col_name)
            self._init_brand_names()

    def _load_brand_items_into_ingredients(self):
        cursor  = self.collection.find({})
        num = 5652
        for doc in cursor:
            for item in doc['items']:
                item['id'] = str(num)
                IngredientsProcessor.add_to_ingredients(item, 'id', 'item_name', True)
                num += 1
                print(num)


    def _init_brand_names(self):
        pos = 0
        for doc in self.collection.find():
            name: str = (doc['name']).lower()
            BrandsProcessor._add_to_brand_name(name, doc['id'])

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