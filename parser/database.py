from pymongo import MongoClient, collection, database
from config import Config


class Database:
    _client = MongoClient(Config.mongo_uri + Config.mongo_username + ':' + Config.mongo_password + '@' + Config.mongo_ip + ':' + Config.mongo_port)

    def __init__(self):
        pass

    @staticmethod
    def get_collection(db_name: str, col_name) -> collection:
        return Database._client[db_name][col_name]
