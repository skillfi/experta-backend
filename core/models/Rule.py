from bson.objectid import ObjectId
from core.config import db
from core.models.base.DbModelBase import DbModelBase
from errors.exceptions import AppBackendError, UnknownIdError
from pymongo.errors import PyMongoError


class Rule(DbModelBase):

    __tablename__ = db.Rules
    
    def __init__(self, fact_id, recommendation) -> 'Rule':
        self.fact_id = fact_id
        self.recommendation = recommendation
    
    @staticmethod
    def add_new(raw: list) -> 'dict':
        """
        Add new Recommendation

        :param dict post_data: Dictionary
        """
        try:
            data = []
            for post_data in raw:
                rule = Rule(
                    fact_id=ObjectId(post_data.get('fact_id')),
                    recommendation=post_data.get('recommendation')
                )
                rule.__tablename__.insert_one(rule.__dict__)
                data.append(rule.__dict__)
            
            return Rule.to_dict_list(data)
        except PyMongoError as ex:
            raise AppBackendError(ex)
    
    @staticmethod
    def del_by_fact_id(rec_id):
        obj = Rule.__tablename__.delete_many({'fact_id': Rule.id(rec_id)})
        return obj.deleted_count
