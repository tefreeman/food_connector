from recipe import Recipe, RecipeFeatures
from probablity import Probability
from typing import List, Dict
from database import Database
from config import Config


class Train:
    _col = Database.get_collection(db_name=Config.recipes_db_name, col_name=Config.recipes_all_col_name)

    @staticmethod
    def calc_accuracy():
        match_count = 0
        non_match_count = 0
        match_count_top_6 = 0
        non_match_count_top_6 = 0
        matches_col = Database.get_collection(Config.matches_db_name, Config.matches_col_name)
        cursor = matches_col.find({})
        for match in cursor:
            if not match['err']:
                recipe: Recipe = Train._get_recipe(match['id'])
                recipe.find_highest_prob_suggestions()
                matches = match['matches']
                suggestions = recipe.suggestions
                length = len(suggestions)
                for i in range(0, length):
                    if matches[i]['err']:
                        continue
                    if len(suggestions[i]) == 0:
                        continue
                    if suggestions[i][0] == matches[i]['id']:
                        match_count += 1
                    else:
                        non_match_count += 1
                    if len(suggestions[i]) < 6:
                        size = len(suggestions[i])
                    else:
                        size = 6
                    matched_6 = False
                    for j in range(0, size):
                        if suggestions[i][j] == matches[i]['id']:
                            matched_6 = True

                    if matched_6:
                        match_count_top_6 += 1
                    else:
                        non_match_count_top_6 += 1
        try:
            return (match_count / (non_match_count + match_count)), (match_count_top_6 / (non_match_count_top_6 + match_count_top_6))
        except:
            return 0


    @staticmethod
    def init_examples():
        matches_col = Database.get_collection(Config.matches_db_name, Config.matches_col_name)
        cursor = matches_col.find({})
        for match in cursor:
            if not match['err']:
                Train.add_to_prob(match['id'], match['matches'])

    @staticmethod
    def add_to_prob(recipe_id: int, matches: List[Dict]):
        recipe = Train._get_recipe(recipe_id)

        if len(recipe.recipe_doc['ingredients']) != len(matches):
            raise Exception("recipe doc ingredients does not match the length of matches")

        recipe_features = recipe.calculate_features()
        ingredient_count = len(recipe_features)
        for i in range(0, ingredient_count):
            for feature in recipe_features[i]:
                if not matches[i]['err']:
                    if feature.ingredient_id == int(matches[i]['id']):
                        Probability.add_example_to_dist(feature, True)
                    else:
                        Probability.add_example_to_dist(feature, False)
        Probability.check_set_feature_status()

    @staticmethod
    def _get_recipe(recipe_id: int) -> Recipe:
        recipe_doc = Train._col.find_one({'id': recipe_id})
        return Recipe(recipe_doc)