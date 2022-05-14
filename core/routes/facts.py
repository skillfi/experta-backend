import os

import core.services.facts as service
from core.config import logger
from core.facts.Engine import System
from core.tools import wrap_response
from flasgger import swag_from
from flask import Blueprint, request

api_facts = Blueprint('api_facts', __name__)
path = os.getcwd()
engine = System()
engine.reset()


@api_facts.route('/api/facts', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/get_all_facts.yaml')
def get_facts_list():
    return wrap_response(service.get_all_facts_endpoint())

@api_facts.route('/api/facts', methods=['POST'])
@swag_from(f'{path}/docs/facts_docs/add_new_fact.yaml')
def add_fact():
    try:
        data = request.form
        # validate form data and skip 'progress' field
        return wrap_response(service.add_fact_endpoint(data))
    except Exception as e:
        # converting error to string
        error = str(e)
        logger.error(error)
        return wrap_response({'errors': {'message': error}})

@api_facts.route('/api/fact/init/<fact_id>', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/get_fact_by_id.yaml', methods=['GET'])
def init_fact(fact_id):
    pass

@api_facts.route('/api/fact/<fact_id>', methods=['GET', 'DELETE'])
@swag_from(f'{path}/docs/facts_docs/get_fact_by_id.yaml', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/get_fact_by_id.yaml', methods=['DELETE'])
def get_delete_update_by_id(fact_id: str):
    if request.method == 'GET':
        return wrap_response(service.get_fact_endpoint(fact_id))
    elif request.method == 'DELETE':
        return wrap_response(service.delete_fact_endpoint(fact_id))
    

