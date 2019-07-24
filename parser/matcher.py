from typing import Dict, List, Set, Tuple
from word import Word
from quantify import quantify_pre_suf
from language_tools import LanguageTools

class Matcher:
    _processed_ingredients: Dict = {}
    _debug_stop_word_count = 0

    def __init__(self):
        pass

    @staticmethod
    def load_processed_ingredients(processed_ingredients):
        Matcher._processed_ingredients = processed_ingredients

    @staticmethod
    def _get_all_ingredients_matches(recipe_ingredients: List[Dict[str, Word]]):
        ingredient_matches: List[List[Tuple[Word, int]]] = []
        for ingredient_list in recipe_ingredients:
            ingredient_matches.append(Matcher._get_ingredient_match(list(ingredient_list.values())))
        return ingredient_matches

    @staticmethod
    def _get_ingredient_match(ingredient_list: List[Word]):
        matches: List[Tuple[Word, int]] = []
        for word_obj in ingredient_list:
            if word_obj.stem in Matcher._processed_ingredients:
                quanti = quantify_pre_suf(word_obj)
                matches.append((Matcher._processed_ingredients[word_obj.stem], quanti))

        # returns the sets
        return matches

    @staticmethod
    def get_all_matches(recipe_ingredients: List[Dict[str, Word]]):
        all_ingredients_matches = Matcher._get_all_ingredients_matches(recipe_ingredients)
        all_matches_by_ids = []
        for ingredient_matches in all_ingredients_matches:
            r_matches = set()
            for i_match in ingredient_matches:
                if i_match[1] >= 0:
                    r_matches = r_matches.union(i_match[0].pos_ingredients)
                else:
                    r_matches = r_matches.union(i_match[0].neg_ingredients)
            all_matches_by_ids.append(r_matches)
        return all_matches_by_ids
