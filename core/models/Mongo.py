from datetime import datetime
from pydoc import doc
from bson.objectid import ObjectId
from core.config import config, db, logger
from core.tools import wrap_response
from errors.exceptions import ExpertaBackendError, UnknownCoollectionIdError


class Mongo:
    """ Kebab Model for storing facts related details """
    __collections__ = {
        'System': db.System,
        'Rules': db.Rules
    }
    fetch_time = datetime.now().strftime(config['DATETIME_FORMAT'])

    def get_by_id(self, _id, collection):
        obj_id = ObjectId(_id)
        response_object = self.__collections__[collection].find_one(obj_id)
        if not response_object:
            raise UnknownCoollectionIdError(_id, collection)
        if isinstance(response_object['_id'], ObjectId):
            response_object['_id'] = str(response_object['_id'])
        return response_object
    
    def get_list(self, collection):
        """
        """
        raw = list()
        all_documents = self.__collections__[collection].find()
        for document in all_documents:
            if isinstance(document['_id'], ObjectId):
                document['_id'] = str(document['_id'])
            raw.append(document)
        return raw
    
    def add_new(self, post_data: dict ,collection):
        try:
            data = dict()
            for k in post_data:
                data[k] = post_data[k]
            data['update_time'] = self.fetch_time
            result = self.__collections__[collection].insert_one(data)
            response_object = {
                'message': 'Successfully added collection.',
                '_id': result.inserted_id
            }
            return wrap_response(response_object)
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return wrap_response({'errors': ex.message}, True)
        except Exception as e:
            error = str(e)
            logger.error(error)
            return wrap_response({'errors': {'message': error}}, True)
    
    def delete_by_id(self, _id, collection):
        object_id = ObjectId(_id)
        query = {'_id': object_id}
        resp = self.__collections__[collection].delete_one(query)
        exclude_fields = ('opTime', 'operationTime', '$clusterTime')
        result = dict()
        res = resp.raw_result
        for fields in res:
            if fields not in exclude_fields:
                result[fields] = res[fields]
        return result
    