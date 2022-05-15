import ast
from datetime import datetime
import uuid

from bson.objectid import ObjectId
from core.config import config, db, logger
from core.facts.Engine import System
from core.tools import wrap_response
from errors.exceptions import ExpertaBackendError, UnknownCoollectionIdError

engine = System()
engine.reset()

class Facts:
    """Facts Model for Storing facts related details"""
    __tablename__ = db.System

    def __init__(self, Meat, Marinade, Coal, Woods, Fire, Weather, Time) -> 'Facts':
        self.Meat = Meat
        self.Marinade = Marinade
        self.Coal = Coal
        self.Woods = Woods
        self.Fire = Fire
        self.Weather = Weather
        self.Time = Time
        self.update_time = datetime.now().strftime(config['DATETIME_FORMAT'])
        # self._id = str(uuid.uuid4())
    
    @property
    def FireBool(self):
        if self.Fire == 'true':
            self.Fire = True
            return self.__dict__
        else:
            self.Fire = False
            return self.__dict__

    @staticmethod
    def id(value):
        return ObjectId(value)

    @staticmethod
    def add_new(post_data: dict) -> 'dict':
        """
        Add new Fact

        :param dict post_data: Dictionary
        """
        try:
            if isinstance(post_data.get('Time'), str) and post_data.get('Time') != '':
                post_data['Time'] = int(post_data['Time'])
            if isinstance(post_data.get('Time'), str) and post_data.get('Time') == '':
                post_data['Time'] = 0
            fact = Facts(
                Meat=post_data.get('Meat'),
                Marinade=post_data.get('Marinade'),
                Coal=post_data.get('Coal'),
                Woods=post_data.get('Woods'),
                Fire=post_data.get('Fire'),
                Weather=post_data.get('Weather'),
                Time=post_data.get('Time')
            )
            result = fact.__tablename__.insert_one(fact.FireBool)
            # fact.id(result.inserted_id)
            response_object = {
                'message': 'Successfully added collection.',
                '_id': str(result.inserted_id)
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
    def get_by_id(fact_id) -> 'dict':
        """
        Get Fact by id

        :param int fact_id: Fact id
        :raise UnknownCoollectionIdError: if Fact not found
        :return: Return Fact by id
        :rtype: UnknownCoollectionIdError or Fact
        """
        response_object = Facts.__tablename__.find_one(Facts.id(fact_id))
        if not response_object:
            raise UnknownCoollectionIdError(fact_id, Facts.__tablename__)
        if isinstance(response_object['_id'], ObjectId):
            response_object['_id'] = str(response_object['_id'])
        return response_object
    
    @staticmethod
    def to_dict_list():
        """
        Transformation Facts column to list

        :param objs: Object to transformation into list
        :return: Return transformed list with values
        :rtype: list
        """
        raw = list()
        all_documents = Facts.__tablename__.find()
        for document in all_documents:
            if isinstance(document['_id'], ObjectId):
                document['_id'] = str(document['_id'])
            raw.append(document)
        return raw

    @staticmethod
    def init_fact_by_id(fact_id) -> 'dict':
        fact_to_rules = Facts.__tablename__.find_one(Facts.id(fact_id))
        engine.init_fact(fact_to_rules)
        engine.run()
    
    @staticmethod
    def init_facts_by_id(first_fact_id, second_fact_id) -> 'dict':
        facts = []
        fact_to_rules = Facts.__tablename__.find_one(Facts.id(first_fact_id))
        second_fact_to_rules = Facts.__tablename__.find_one(Facts.id(second_fact_id))
        facts.append(fact_to_rules)
        facts.append(second_fact_to_rules)
        engine.init_fact(fact_to_rules, True, len(facts), facts)
        return engine.run()

    
    @staticmethod
    def delete_by_id(fact_id) -> 'dict':
        query = {'_id': Facts.id(fact_id)}
        resp = Facts.__tablename__.delete_one(query)
        exclude_fields = ('opTime', 'operationTime', '$clusterTime', 'electionId')
        result = dict()
        res = resp.raw_result
        for fields in res:
            if fields not in exclude_fields:
                result[fields] = res[fields]
        return result
