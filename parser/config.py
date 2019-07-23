from configparser import ConfigParser


class Config:
    _config = ConfigParser()
    
    mongo_uri = ""
    mongo_ip = ""
    mongo_port = ""
    mongo_auth = ""
    mongo_username = ""
    mongo_password = ""

    nutritionix_db_name = ""
    food_col_name = ""
    grocery_col_name = ""
    food_all_col_name = ""

    ingredient_db_name = ""
    processed_ingredients_col_name = ""

    recipes_db_name = ""
    recipes_all_col_name = ""

    matches_db_name = ""
    matches_col_name = ""
    
    @staticmethod
    def load_config(url: str):
        Config._config.read(url)
        Config.mongo_uri = Config._config.get('Mongo', 'uri')
        Config.mongo_ip = Config._config.get('Mongo', 'ip')
        Config.mongo_port = Config._config.get('Mongo', 'port')
        Config.mongo_auth = Config._config.getboolean('Mongo', 'auth')
        Config.mongo_username = Config._config.get('Mongo', 'username')
        Config.mongo_password = Config._config.get('Mongo', 'password')

        Config.nutritionix_db_name = Config._config.get('Nutritionix_Db', 'db_name')
        Config.food_col_name = Config._config.get('Nutritionix_Db', 'food_col_name')
        Config.grocery_col_name = Config._config.get('Nutritionix_Db', 'grocery_col_name')
        Config.food_all_col_name = Config._config.get('Nutritionix_Db', 'all_food_col_name')

        Config.ingredient_db_name = Config._config.get('Ingredients_Db', 'db_name')
        Config.processed_ingredients_col_name = Config._config.get('Ingredients_Db', 'col_processed_name')

        Config.recipes_db_name = Config._config.get('Recipes_Db', 'db_name')
        Config.recipes_all_col_name = Config._config.get('Recipes_Db', 'recipes_all_name')

        Config.matches_db_name = Config._config.get('Matches_Db', 'db_name')
        Config.matches_col_name = Config._config.get('Matches_Db', 'col_matches')