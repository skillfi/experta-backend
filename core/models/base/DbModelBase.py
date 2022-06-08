from pymongo.errors import PyMongoError
from core.config import db
from errors.exceptions import AppBackendError
from bson.objectid import ObjectId

class DbModelBase:
    @staticmethod
    def id(value):
        return ObjectId(value)

    @classmethod
    def get_by_id(cls, rec_id):
        try:
            obj = cls.__tablename__.find_one(cls.id(rec_id))
        except PyMongoError as ex:
            raise AppBackendError(ex)
        return obj

    @classmethod
    def get_list(cls):
        return cls.__tablename__.find()
    
    @classmethod
    def get_list_by_query(cls, query: dict):
        return cls.__tablename__.find(query)
    
    @classmethod
    def del_by_id(cls, rec_id):
        query = {'_id': cls.id(rec_id)}
        obj = cls.__tablename__.delete_one(query)
        return obj.deleted_count
    
    @staticmethod
    def to_dict_list(objs):
        result = list()
        for documents in objs:
            for key in documents:
                if isinstance(documents[key], ObjectId):
                    documents[key] = str(documents[key])
            result.append(documents)
        return result