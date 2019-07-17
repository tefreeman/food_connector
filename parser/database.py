from pymongo import MongoClient, collection, database
from config import Config
from typing import List, Set, Dict


class Database:
    _config = Config()
    _client = MongoClient(_config.mongo_uri + _config.mongo_username + ':' + _config.mongo_password + '@' + _config.mongo_ip + ':' + _config.mongo_port)

    def __init__(self):
        pass

    @staticmethod
    def get_collection(db_name: str, col_name) -> collection:
        return Database._client[db_name][col_name]


