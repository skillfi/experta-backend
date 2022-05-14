from datetime import datetime

from bson.objectid import ObjectId
from core.config import config, db, logger
from core.facts.Engine import System
from errors.exceptions import ExpertaBackendError, UnknownCoollectionIdError

engine = System()
engine.reset()


# class Mongo:
#     """ collections Model for storing facts related details """
#     __collections__ = {
#         'System': db.System,
#         'Rules': db.Rules
#     }
#     fetch_time = datetime.now().strftime(config['DATETIME_FORMAT'])

#     Meat = 'Meat'
#     Action = 'Action'
#     DegreeOfReadiness = 'DegreeOfReadiness'
#     Pardone = 'Pardone'
#     TurnedOver = 'TurnedOver'
#     CookedFor = 'CookedFor'
#     Time = 'Time'
#     def get_by_id(self, _id, collection):
#         obj_id = ObjectId(_id)
#         response_object = self.__collections__[collection].find_one(obj_id)
#         if not response_object:
#             raise UnknownCoollectionIdError(_id, collection)
#         if isinstance(response_object['_id'], ObjectId):
#             response_object['_id'] = str(response_object['_id'])
#         return response_object
    
#     def get_list(self, collection):
#         """
#         """
#         raw = list()
#         all_documents = self.__collections__[collection].find()
#         for document in all_documents:
#             if isinstance(document['_id'], ObjectId):
#                 document['_id'] = str(document['_id'])
#             raw.append(document)
#         return raw
    
#     def add_new(self, post_data: dict ,collection):
#         """
#         Add new fiil collection list:\n
#         `System` and    `Rules`
#         """
#         try:
#             data = dict()
#             for k in post_data:
#                 data[k] = post_data[k]
#             data['update_time'] = self.fetch_time
#             result = self.__collections__[collection].insert_one(data)
#             response_object = {
#                 'message': 'Successfully added collection.',
#                 '_id': result.inserted_id
#             }
#             return wrap_response(response_object)
#         except ExpertaBackendError as ex:
#             logger.error(ex.message)
#             return wrap_response({'errors': ex.message}, True)
#         except Exception as e:
#             error = str(e)
#             logger.error(error)
#             return wrap_response({'errors': {'message': error}}, True)
    
#     def delete_by_id(self, _id, collection):
#         object_id = ObjectId(_id)
#         query = {'_id': object_id}
#         resp = self.__collections__[collection].delete_one(query)
#         exclude_fields = ('opTime', 'operationTime', '$clusterTime', 'electionId')
#         result = dict()
#         res = resp.raw_result
#         for fields in res:
#             if fields not in exclude_fields:
#                 result[fields] = res[fields]
#         return result
    
#     @staticmethod
#     def get_by_index(index, data):
#         pass

class Facts:
    """Facts Model for Storing facts related details"""
    __tablename__ = db.System

    def __init__(self, Meat, Action, DegreeOfReadiness, Pardone, TurnedOver, CookedFor, Time) -> 'Facts':
        self.Meat = Meat
        self.Action = Action
        self.DegreeOfReadiness = DegreeOfReadiness
        self.Pardone = Pardone
        self.TurnedOver = TurnedOver
        self.CookedFor = CookedFor
        self.Time = Time
        self.update_time = datetime.now().strftime(config['DATETIME_FORMAT'])
        self._id = ''
    
    @property
    def Turned(self):
        if self.TurnedOver == 'true':
            self.TurnedOver = True
            return self.__dict__
        else:
            self.TurnedOver = False
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
            fact = Facts(
                Meat=post_data.get('Meat'),
                Action=post_data.get('Action'),
                DegreeOfReadiness=post_data.get('DegreeOfReadiness'),
                Pardone=post_data.get('Pardone'),
                TurnedOver=post_data.get('TurnedOver'),
                CookedFor=post_data.get('CookedFor'),
                Time=post_data.get('Time')
            )
            result = fact.__tablename__.insert_one(fact.__dict__)
            fact.id(result.inserted_id)
            response_object = {
                'message': 'Successfully added collection.',
                '_id': result.inserted_id
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
    def delete_by_id(fact_id):
        query = {'_id': Facts.id(fact_id)}
        resp = Facts.__tablename__.delete_one(query)
        exclude_fields = ('opTime', 'operationTime', '$clusterTime', 'electionId')
        result = dict()
        res = resp.raw_result
        for fields in res:
            if fields not in exclude_fields:
                result[fields] = res[fields]
        return result
