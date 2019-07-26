from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from typing import Dict, List
from flask import jsonify
import pymongo
from config import Config
from database import Database
from bson.json_util import dumps
from matcher import Matcher
from recipe import Recipe
from train import Train
from helpers import open_file_as_text
from probablity import Probability
from ingredients_processor import IngredientsProcessor
app = Flask(__name__)
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/get_random')
def get_random_recipe():
    col = Database.get_collection(db_name=Config.recipes_db_name, col_name=Config.recipes_all_col_name)
    recipe_doc = list(col.aggregate([{ '$sample': { 'size': 1 } },{ '$match': { 'isMatched': False } }]))[0]

    recipe = Recipe(recipe_doc)
    recipe.find_highest_prob_suggestions(8)

    recipe_doc['suggestions'] = recipe.suggestions

    return dumps(recipe_doc)


@app.route('/submit_recipe_match', methods=['POST'])
def submit_match():
    recipe_col = Database.get_collection(db_name=Config.recipes_db_name, col_name=Config.recipes_all_col_name)
    matches_col = Database.get_collection(db_name=Config.matches_db_name, col_name=Config.matches_col_name)
    req_data = request.get_json()
    recipe_id = req_data['id']

    result = recipe_col.update_one({'id': recipe_id}, {'$set': {'isMatched': True}})
    result_1 = matches_col.insert(req_data)

    if not req_data['err']:
        Train.add_to_prob(recipe_id, req_data['matches'])

    if result.modified_count != 1:
        print('modified count is not 1')

    return get_random_recipe()


@app.route('/get_ingredients_dir')
def get_ingredients_dir():
    return open_file_as_text('i_dir.txt')


@app.route('/get_ingredients_tree')
def get_ingredients_tree():
    return open_file_as_text('i_tree.txt')


@app.route('/get_prob_info')
def get_prob_info():
    pass
