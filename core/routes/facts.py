import os

from core.config import logger
from core.facts.Engine import System
from core.models.Mongo import Mongo
from core.tools import wrap_response
from errors.exceptions import ExpertaBackendError
from flasgger import swag_from
from flask import Blueprint, request

api_facts = Blueprint('api_facts', __name__)
api_rules = Blueprint('api_rules', __name__)
path = os.getcwd()
engine = System()
engine.reset()


@api_facts.route('/api/facts', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/get_all_facts.yaml')
def get_facts_list():
    try:
        db = Mongo()
        facts = db.get_list('System')
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return wrap_response({'errors': ex.message}, True)
    
    return wrap_response(facts)

@api_facts.route('/api/fact/init', methods=['POST'])
@swag_from(f'{path}/docs/facts_docs/add_new_fact.yaml')
def add_fact():
    try:
        data = request.form
        Turned = False
        if data.get('TurnedOver') == 'true':
            Turned = True
        result = engine.init_fact(data, Turned)
        engine.run()
    except Exception as e:
        error = str(e)
        logger.error(error)
        resp = {
            'errors': {
                'message': error
            }
        }
        return wrap_response(resp, True)
    return result

@api_facts.route('/api/fact/<_id>', methods=['GET', 'DELETE'])
@swag_from(f'{path}/docs/facts_docs/get_fact_by_id.yaml', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/get_fact_by_id.yaml', methods=['DELETE'])
def get_delete_update_by_id(_id: str):
    result = None
    db = Mongo()
    try:
        if request.method == 'GET':
            result = db.get_by_id(_id, 'System')
        elif request.method == 'DELETE':
            result = db.delete_by_id(_id, 'System')
            if not result:
                error = {'message': f'Fact with _id = {_id} does not exist'}
                logger.error(error)
                return wrap_response({'errors': error}, True)
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return wrap_response({'errors': ex.message}, True)
    except Exception as e:
        error = str(e)
        resp = {
            'errors': {
                'message': error
            }
        }
        return wrap_response(resp, True)
    
    return wrap_response([result])

@api_rules.route('/api/rules', methods=['GET'])
@swag_from(f'{path}/docs/rules_docs/get_all_rules.yaml')
def get_facts_list():
    try:
        db = Mongo()
        facts = db.get_list('Rules')
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return wrap_response({'errors': ex.message}, True)
    
    return wrap_response(facts)