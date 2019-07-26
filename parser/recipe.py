from typing import Dict, Set
import pymongo
from language_tools import LanguageTools, B_Word
from word import Word
from quantify import quantify_pre_suf
from matcher import Matcher
from typing import List
from ingredients_processor import IngredientsProcessor
from probablity import Probability, KeyType, ProbFeatureKeys
from operator import itemgetter


class RecipeFeatures:
    _ingredients_db_list: Dict = IngredientsProcessor.get_ingredients_as_key_list()

    def __init__(self, ingredient_id: int, recipe_words: Dict[str, Word]):
        self.ingredient_id = ingredient_id
        self.recipe_ingredients_words = recipe_words
        self.ingredients_db_words = RecipeFeatures._ingredients_db_list[str(ingredient_id)]

        # features (relative is match - non matching ingredients words (from db))
        self.match_count = 0
        self.non_match_count = 0
        self.rel_match_count = 0

        # freq matches / non matches
        self.match_freq = 0

        #
        # recipe ingredient word not in ingredient DB
        self.unknown_match_count = 0

        self.match_g_tag: Dict = {}
        self.match_tree_count = {}

        # computes matches & non matches at depth of match tree
        self.match_tree_depth_count = [[0, 0] for _ in range(100)]
        self.match_tree_depth_freq = []

        self.total_match_freq = 0
        self.total_non_match_freq = 0
        self.avg_match_freq = 0

        self.avg_non_match_freq = 0

        self.add_match_features()
        self.calc_not_match_features()
        self.calculate_averages()
        self.calculate_frequencies()

    def add_match_features(self):
        for ri_word in list(self.recipe_ingredients_words.values()):
            if ri_word.stem in self.ingredients_db_words:
                self.rel_match_count += 1
                self.match_count += 1
                RecipeFeatures._add_to_dict(ri_word.g_tag, self.match_g_tag)
                RecipeFeatures._merge_to_set(ri_word.tree, self.match_tree_count)
                RecipeFeatures._merge_to_list(ri_word.tree, self.match_tree_depth_count, 1)
                self.total_match_freq += ri_word.freq
            else:
                self.unknown_match_count += 1

    def get_as_dict(self):
        p = ProbFeatureKeys
        return {p.MATCH_COUNT.name: self.match_count, p.NON_MATCH_COUNT.name: self.non_match_count, p.REL_MATCH_COUNT.name: self.rel_match_count, p.MATCH_FREQ.name: self.match_freq,
                p.UNKNOWN_MATCH_COUNT.name: self.unknown_match_count, p.MATCH_G_TAG.name: self.match_g_tag, p.MATCH_TREE_COUNT.name: self.match_tree_count, p.MATCH_TREE_DEPTH_FREQ.name: self.match_tree_depth_freq}

    def calc_prob(self):
        return Probability.calculate_prob(self)

    # is_match = 1: positive, is_match = 0: negative
    @staticmethod
    def _merge_to_list(x: List[List[str]], g_li: List, is_match: int):
        for li in x:
            length = len(li)
            for i in range(0, length):
                g_li[i][is_match] += 1

    @staticmethod
    def _add_to_dict(x: str, d: Dict, pos=0):
        if x not in d:
            d[x] = [0, 0]
        d[x][pos] += 1

    @staticmethod
    def _add_to_list(i: int, d: list, length: int, pos=0):
        d_length = len(d)
        if d_length < length:
            for i in range(d_length, length):
                d[i] = [0, 0]
        d[i][pos] += 1

    @staticmethod
    def _merge_to_dict(x: List[str], d: Dict, pos=0):
        for li in x:
            length = len(li)
            for i in range(0, length):
                RecipeFeatures._add_to_dict(li[i], d, pos)

    @staticmethod
    def _merge_to_set(s: Set[str], d: dict, pos=0):
        for word in s:
            RecipeFeatures._add_to_dict(word, d, pos)

    def calculate_frequencies(self):
        self.match_freq = self.match_count / (self.non_match_count + self.match_count)

        for depth_match in self.match_tree_depth_count:
            if depth_match[0] + depth_match[1] != 0:
                self.match_tree_depth_freq.append(depth_match[1] / (depth_match[0] + depth_match[1]))
            else:
                self.match_tree_depth_freq.append(0)

        for item in self.match_g_tag.items():
            self.match_g_tag[item[0]] = item[1][0] / (item[1][1] + item[1][0])

    def calculate_averages(self):
        self.avg_match_freq = self.total_match_freq / self.match_count
        # need to test how to remove added bias by forcing to 0 when attempting to divide by 0
        if self.non_match_count == 0:
            self.avg_non_match_freq = 0
        else:
            self.avg_non_match_freq = self.total_non_match_freq / self.non_match_count

    def calc_not_match_features(self):
        for i_word in list(self.ingredients_db_words.values()):
            if i_word.stem not in self.recipe_ingredients_words:
                self.non_match_count += 1
                self.rel_match_count -= 1
                RecipeFeatures._add_to_dict(i_word.g_tag, self.match_g_tag, 1)
                RecipeFeatures._merge_to_dict(i_word.tree, self.match_tree_count, 1)
                RecipeFeatures._merge_to_list(i_word.tree, self.match_tree_depth_count, 0)
                self.total_non_match_freq += i_word.freq


class Recipe:
    _matcher: Matcher = Matcher()

    def __init__(self, recipe_doc):
        self.recipe_doc = recipe_doc
        self.r_ingredients = self._build_words_list()
        self.suggestions = None

    def calculate_features(self) -> List[List[RecipeFeatures]]:
        r_features: List[List[RecipeFeatures]] = []
        matches = self._find_matches()
        length = len(matches)
        for i in range(0, length):
            r_features.append([])
            for match in matches[i]:
                r_features[i].append(RecipeFeatures(match, self.r_ingredients[i]))
        return r_features

    def find_highest_prob_suggestions(self, max_count: int = None):
        suggestions = []
        ingredients_features = self.calculate_features()
        pos = 0
        for ingredient_features in ingredients_features:
            suggestions.append([])
            for feature in ingredient_features:
                prob = feature.calc_prob()
                suggestions[pos].append({str(feature.ingredient_id): prob})
            suggestions[pos].sort(key=lambda x: list(x.values())[0], reverse=True)
            if max_count is not None:
                suggestions[pos] = suggestions[pos][0:max_count]
            pos += 1
        self.suggestions = Recipe._format_suggestions(suggestions)

    @staticmethod
    def _format_suggestions(recipe_suggestions):
        for ingredient_suggestions in recipe_suggestions:
            suggestions_len = len(ingredient_suggestions)
            for i in range(0, suggestions_len):
                ingredient_id = list(ingredient_suggestions[i].keys())[0]
                ingredient_suggestions[i] = ingredient_id
        return recipe_suggestions

    def _build_words_list(self):
        recipe_ingredients: List[Dict[str, Word]] = []
        for ingredient_text in self.recipe_doc['ingredients']:
            ingredients: Dict[str, Word] = {}
            words_dict = LanguageTools.return_base_words_from_string(ingredient_text.lower())
            words_dict = LanguageTools.filter_words(words_dict)
            for word_dict in words_dict:
                ingredients[word_dict.stem] = Word(word_dict.word, word_dict.stem, word_dict.g_tag, False)
            recipe_ingredients.append(ingredients)
        return recipe_ingredients


    def _find_matches(self):
        return Matcher.get_all_matches(self.r_ingredients)
