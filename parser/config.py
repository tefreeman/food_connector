from configparser import ConfigParser


class _Config:
    _config = ConfigParser()
    _instance = None

    def __init__(self):
        _Config._config.read('./config.ini')
        self.mongo_uri = _Config._config.get('Mongo', 'uri')
        self.mongo_ip = _Config._config.get('Mongo', 'ip')
        self.mongo_port = _Config._config.get('Mongo', 'port')
        self.mongo_auth = _Config._config.getboolean('Mongo', 'auth')
        self.mongo_username = _Config._config.get('Mongo', 'username')
        self.mongo_password = _Config._config.get('Mongo', 'password')

        self.nutritionix_db_name = _Config._config.get('Nutritionix_Db', 'db_name')
        self.food_col_name = _Config._config.get('Nutritionix_Db', 'food_col_name')
        self.grocery_col_name = _Config._config.get('Nutritionix_Db', 'grocery_col_name')

        self.ingredient_db_name = _Config._config.get('Ingredients_Db', 'db_name')
        self.processed_ingredients_col_name = _Config._config.get('Ingredients_Db', 'col_processed_name')

        self.recipes_db_name = _Config._config.get('Recipes_Db', 'db_name')
        self.recipes_all_col_name = _Config._config.get('Recipes_Db', 'recipes_all_name')

        self.matches_db_name = _Config._config.get('Matches_Db', 'db_name')
        self.matches_col_name = _Config._config.get('Matches_Db', 'col_matches')


def Config() -> _Config:
    if _Config._instance is None:
        _Config._instance = _Config()
    return _Config._instance