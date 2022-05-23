from bson.objectid import ObjectId
from core.config import db, logger
from core.tools import wrap_response
from errors.exceptions import ExpertaBackendError, UnknownCoollectionIdError



class Rule:

    __tablename__ = db.Rules
    
    def __init__(self, fact_id, recommendation) -> 'Rule':
        self.fact_id = fact_id
        self.recommendation = recommendation
    
    @staticmethod
    def add_new(raw: list, engine) -> 'dict':
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
                
            response_object = {
                'message': 'Successfully added collection.'
            }
            return response_object
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return {'errors': ex.message}
        except Exception as e:
            error = str(e)
            logger.error(error)
            return {'errors': {'message': error}}
    
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
    def get_by_fact_id(fact_id) -> 'dict':
        """
        Get Rule by fact_id

        :param int fact_id: Fact id
        :raise UnknownCoollectionIdError: if Rule not found
        :return: Return Rule by fact_id
        :rtype: UnknownCoollectionIdError or Rule
        """
        rule = Rule.__tablename__.find({'fact_id':Rule.id(fact_id)})
        if not rule:
            raise UnknownCoollectionIdError(fact_id, Rule.__tablename__)
        raw = list()
        for rul in rule:
            if isinstance(rul['_id'], ObjectId):
                rul['_id'] = str(rul['_id'])
                rul['fact_id'] = str(rul['fact_id'])
            raw.append(rul)
        return raw
    
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
            if isinstance(document['_id'], ObjectId) and isinstance(document['fact_id'], ObjectId):
                document['_id'] = str(document['_id'])
                document['fact_id'] = str(document['fact_id'])
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
