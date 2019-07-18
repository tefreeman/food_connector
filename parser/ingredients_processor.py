from typing import List, Dict
from language_tools import LanguageTools
from quantify import quantify_pre_suf
from word import Word
from config import Config
from database import Database
from matcher import Matcher
import copy
from helpers import getsize


class IngredientsProcessor:
    _ingredients_dict_words: Dict = {}
    _ingredients_words_list: Dict = {}

    _raw_ingredients: Dict = {}

    ingredients_dir: Dict = {}
    ingredients_tree: Dict = {}

    _loaded = False

    def __init__(self):
        IngredientsProcessor._load_ingredients_from_db()

    @staticmethod
    def _load_ingredients_from_db():
        if not IngredientsProcessor._loaded:
            col = Database.get_collection(Config().nutritionix_db_name, Config().food_col_name)
            cursor = col.find({})
            for ingredient in cursor:
                IngredientsProcessor.add_to_ingredients(ingredient)
                IngredientsProcessor._add_to_raw_ingredients(ingredient)
                IngredientsProcessor._add_to_ingredients_dir(ingredient)
            print("IngredientsProcessor:  ingredients Loaded!")
            # auto load into Matcher
            Matcher.load_processed_ingredients(IngredientsProcessor.get_ingredients_as_dict())
        else:
            print("Class IngredientsProcessor, _load_ingredients_from_db method has already been called")
        print(' ingredients dict words: ', getsize(IngredientsProcessor._ingredients_dict_words))
        print(' ingredients words list: ', getsize(IngredientsProcessor._ingredients_words_list))
        print(' ingredients tree: ', getsize(IngredientsProcessor.ingredients_tree))

    @staticmethod
    def _add_to_ingredients_dir(ingredient: Dict):
        if ingredient['id'] not in IngredientsProcessor.ingredients_tree:
            IngredientsProcessor.ingredients_dir[str(ingredient['id'])] = ingredient['food_name']
        else:
            print("possible error: ingredient_id in func: _add_to_ingredients_dir in "
                  " class IngredientsProcessor has already been defined")

    @staticmethod
    def _add_to_ingredients_tree(ingredient_id, word_objs: Dict[str, Word]):
        for word_obj in word_objs.items():
            word = word_obj[1]
            if word.stem not in IngredientsProcessor.ingredients_tree:
                IngredientsProcessor.ingredients_tree[word.stem] = {}
            IngredientsProcessor.ingredients_tree[word.stem][str(ingredient_id)] = 0

    @staticmethod
    def _add_to_raw_ingredients(ingredient: Dict):
        IngredientsProcessor._raw_ingredients[str(ingredient['id'])] = ingredient

    @staticmethod
    def _set_ingredient_ids():
        id_num = 0
        for word_obj in IngredientsProcessor._ingredients_dict_words.values():
            word_obj.id = id_num
            id_num += 1

    @staticmethod
    def add_to_ingredients(ingredient: Dict):
        ingredient_id: int = ingredient['id']
        stemmed_words = LanguageTools.return_base_words_from_string(ingredient['food_name'])

        word_objs: Dict[Word] = {}
        for stemmed_word in stemmed_words:
            word_obj = Word(stemmed_word['word'], stemmed_word['stem'], stemmed_word['g_tag'])
            quantified_val = quantify_pre_suf(word_obj)

            word_objs[word_obj.stem] = word_obj
            if word_obj.stem not in IngredientsProcessor._ingredients_dict_words:
                IngredientsProcessor._ingredients_dict_words[word_obj.stem] = word_obj

            IngredientsProcessor._ingredients_dict_words[word_obj.stem].add_ingredient_id(ingredient_id, quantified_val)

        IngredientsProcessor._ingredients_words_list[str(ingredient_id)] = word_objs
        IngredientsProcessor._add_to_ingredients_tree(ingredient_id, word_objs)
        IngredientsProcessor._set_ingredient_ids()

    @staticmethod
    def get_ingredients_as_dict():
        return copy.deepcopy(IngredientsProcessor._ingredients_dict_words)

    @staticmethod
    def get_ingredients_as_list() -> List[Word]:
        return list(IngredientsProcessor._ingredients_dict_words.values())

    @staticmethod
    def get_ingredients_as_json() -> List[Dict]:
        json_ingredients = []
        ingredients_list = IngredientsProcessor.get_ingredients_as_list()

        for ingredient in ingredients_list:
            json_ingredients.append(ingredient.to_json())

        return json_ingredients

    @staticmethod
    def get_ingredients_as_key_list() -> Dict[str, Dict[str, Word]]:
        return IngredientsProcessor._ingredients_words_list

    @staticmethod
    def get_ingredient_by_id(ingredient_id: str):
        return IngredientsProcessor._raw_ingredients[ingredient_id]
