from typing import List, Dict, NamedTuple
from language_tools import LanguageTools
from quantify import quantify_pre_suf
from word import Word
from config import Config
from database import Database
from matcher import Matcher
from helpers import getsize, save_json_to_file
from ingredient import Ingredient, IngredientTuple


class IngredientsProcessor:
    # word tree structure
    _ingredients_dict_words: Dict = {}
    # id (number): dict[words]
    _ingredients_words_list: Dict = {}

    # id (number): name (str)
    ingredients_dir: Dict = {}

    # word.stem : Dict[id, 0]
    ingredients_tree: Dict = {}

    _loaded = False

    def __init__(self):
        IngredientsProcessor._load_food_ingredients()

    @staticmethod
    def _load_food_ingredients():
        if not IngredientsProcessor._loaded:
            col = Database.get_collection(Config.nutritionix_db_name, Config.food_all_col_name)
            cursor = col.find({'is_item': False})
            Ingredient.init_list_size(cursor.count())

            for i_doc in cursor:
                Ingredient.add_to_ingredients(i_doc)

        IngredientsProcessor._build_structures()
        IngredientsProcessor._write_server_files()
        IngredientsProcessor._loaded = True

    @staticmethod
    def _build_structures():
        for ingredient in Ingredient.get_all_ingredients():
            IngredientsProcessor.add_to_ingredients(ingredient)
            IngredientsProcessor._add_to_ingredients_dir(ingredient)

        Matcher.load_processed_ingredients(IngredientsProcessor.get_ingredients_as_dict())

    @staticmethod
    def _add_to_ingredients_dir(ingredient: IngredientTuple):
        if ingredient.id not in IngredientsProcessor.ingredients_tree:
            IngredientsProcessor.ingredients_dir[str(ingredient.id)] = ingredient.name
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
    def _set_ingredient_ids():
        id_num = 0
        for word_obj in IngredientsProcessor._ingredients_dict_words.values():
            word_obj.id = id_num
            id_num += 1

    @staticmethod
    def add_to_ingredients(ingredient: IngredientTuple):
        ingredient_id: int = ingredient.id
        stemmed_words = LanguageTools.return_base_words_from_string(ingredient.name)

        word_objs: Dict[Word] = {}

        for stemmed_word in stemmed_words:
            word_obj = Word(stemmed_word.word, stemmed_word.stem, stemmed_word.g_tag, ingredient.is_item)
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
        return IngredientsProcessor._ingredients_dict_words

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
    def _write_server_files():
        save_json_to_file('i_dir.txt', IngredientsProcessor.ingredients_dir)
        save_json_to_file('i_tree.txt', IngredientsProcessor.ingredients_tree)

        del IngredientsProcessor.ingredients_tree
        del IngredientsProcessor.ingredients_dir

    @staticmethod
    def get_ingredients_as_key_list() -> Dict[str, Dict[str, Word]]:
        return IngredientsProcessor._ingredients_words_list
