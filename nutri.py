from database import Database
from config import Config


class Nutri:
    #TODO add_all_collection
    _items_nutrients  = {}

    @staticmethod
    def calc_nutri_similarity(id_1, id_2):
        item1 = Nutri._items_nutrients[id_1]
        item2 = Nutri._items_nutrients[id_2]

