from typing import Dict, List, NamedTuple
from collections import namedtuple


class IngredientTuple(NamedTuple):
    id: int
    name: str
    is_item: bool
    upc: int
    ingredient_statement: str
    serving_qty: int
    serving_unit: str
    serving_weight: int
    metric_qty: int
    metric_unit: str
    brand_name: str
    food_group: int
    measures: List
    nutrients: Dict


class Ingredient:
    _ingredients: List[IngredientTuple] = None

    @staticmethod
    def init_list_size(num_docs: int):
        Ingredient._ingredients = [None] * num_docs

    @staticmethod
    def add_to_ingredients(i_doc: Dict):
        i_tuple = Ingredient._transform_to_tuple(i_doc)
        Ingredient._ingredients[i_tuple.id] = i_tuple

    @staticmethod
    def _transform_to_tuple(i: Dict) -> IngredientTuple:
        return IngredientTuple(id=i['id'], name=i['name'], is_item = i['is_item'], upc=i['upc'],
                       ingredient_statement=i['ingredient_statement'], serving_qty=i['serving_qty'],
                       serving_unit=i['serving_unit'], serving_weight=i['serving_weight'], metric_qty=i['metric_qty'],
                       metric_unit=i['metric_unit'], brand_name=i['brand_name'], food_group=i['food_group'],
                       measures=i['measures'], nutrients=i['nutrients']
                       )

    @staticmethod
    def get_all_ingredients() -> List[IngredientTuple]:
        return Ingredient._ingredients

    @staticmethod
    def get_ingredient(id_num: int):
        return Ingredient._ingredients[id_num]