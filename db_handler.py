import pymongo
from user import User, HeartStyle
from typing_extensions import override
import logging
from abc import ABC

from logger import create_logger

logger = create_logger('db_handler', 'db_handler.log')

class DBHandler(ABC):
    def __init__(self):
        pass

    def get_user(user_id : str) -> User:
        pass

    def update_user(self, user : User) -> None:
        pass

class MongoDBHandler(DBHandler):
    def __init__(self,
                db_name = "test_db",
                db_url = 'mongodb://localhost:27017/',
            ):
        super().__init__()
        logger.info('Initializing Mongo DB...')
        self.db_name = db_name
        self.db_url = db_url
        self._client = pymongo.MongoClient('localhost', 27017)
        self._db = self._client[db_name]
        logger.info('Mongo DB initialized...')

    @override
    def get_user(self, user_id : str, username : str = "") -> User:
        users_col_name = 'users'
        cur_user = self._db[users_col_name].find_one({"user_id" : user_id})
        logger.info(f'found user: {cur_user}')
        if not cur_user:
            self._db[users_col_name].insert_one({
                'user_id' : user_id,
                'username' : username,
                'heart_style' : HeartStyle().to_dict()
            })
            logger.info(f'created user: {user_id}')
            return User(
                username,
                user_id,
                HeartStyle()
            )

        return User(
            username,
            user_id,
            HeartStyle(
                cur_user['heart_style']['style'],
                cur_user['heart_style']['form'],
                cur_user['heart_style']['color'],
                cur_user['heart_style']['props'],
                cur_user['heart_style']['size']
            )
        )

    @override
    def update_user(self, user : User) -> None:
        users_col_name = 'users'
        self._db[users_col_name].update_one(
            {"user_id" : user.user_id},
            {
                "$set" : {
                    "username" : user.username,
                    "heart_style" : user.heart_style.to_dict()
                }
            }
        )
