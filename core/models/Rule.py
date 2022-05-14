from bson.objectid import ObjectId
from core.config import db
from errors.exceptions import UnknownCoollectionIdError


class Rule:

    __tablename__ = db.Rules
    
    def __init__(self, CE, Pattern) -> 'Rule':
        self.CE = CE
        self.Pattern = Pattern
    
    @staticmethod
    def id(value):
        return ObjectId(value)
    
    @staticmethod
    def get_by_id(rule_id) -> 'dict':
        """
        Get Rule by id

        :param int rule_id: Rule id
        :raise UnknownCoollectionIdError: if Rule not found
        :return: Return Rule by id
        :rtype: UnknownCoollectionIdError or Rule
        """
        response_object = Rule.__tablename__.find_one(Rule.id(rule_id))
        if not response_object:
            raise UnknownCoollectionIdError(rule_id, Rule.__tablename__)
        if isinstance(response_object['_id'], ObjectId):
            response_object['_id'] = str(response_object['_id'])
        return response_object
    
    @staticmethod
    def to_dict_list():
        """
        Transformation Rules column to list

        :param objs: Object to transformation into list
        :return: Return transformed list with values
        :rtype: list
        """
        raw = list()
        all_documents = Rule.__tablename__.find()
        for document in all_documents:
            if isinstance(document['_id'], ObjectId):
                document['_id'] = str(document['_id'])
            raw.append(document)
        return raw
    
    @staticmethod
    def delete_by_id(fact_id):
        query = {'_id': Rule.id(fact_id)}
        resp = Rule.__tablename__.delete_one(query)
        exclude_fields = ('opTime', 'operationTime', '$clusterTime', 'electionId')
        result = dict()
        res = resp.raw_result
        for fields in res:
            if fields not in exclude_fields:
                result[fields] = res[fields]
        return result
