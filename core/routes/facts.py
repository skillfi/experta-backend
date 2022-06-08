import os

import core.services.facts as service
import core.services.rules as service_rule
from core.config import logger
from core.facts.Engine import System
from core.tools import wrap_response
from flasgger import swag_from
from flask import Blueprint, request

api_facts = Blueprint('api_facts', __name__)
path = os.getcwd()


@api_facts.route('/api/facts', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/get_all_facts.yaml')
def get_facts_list():
    return wrap_response(service.get_all_facts_endpoint())


@api_facts.route('/api/facts', methods=['POST'])
@swag_from(f'{path}/docs/facts_docs/add_new_fact.yaml')
def add_fact():
    data = request.form
    object = dict(
        Meat=data.get('Meat').split(','),
        Marinade=[data.get('Marinade')],
        Coal=data.get('Coal').split(','),
        Woods=data.get('Woods').split(','),
        Weather=data.get('Weather').split(','),
        Fire=data.get('Fire'),
        Time=data.get('Time', 0)
    )
    # validate form data and skip 'progress' field
    return wrap_response(service.add_fact_endpoint(object))


@api_facts.route('/api/fact/get-recommendation/<fact_id>', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/init_fact_by_id.yaml', methods=['GET'])
def init_fact(fact_id):
    service.init_fact_endpoint(fact_id)
    if len(service_rule.get_rule_by_fact_endpoint(fact_id)) > 0:
        return wrap_response(service_rule.get_rule_by_fact_endpoint(fact_id))
    service.init_fact_endpoint(fact_id)
    return wrap_response(service_rule.get_rule_by_fact_endpoint(fact_id))


@api_facts.route('/api/fact/get-recommendation/<first_fact_id>/and/<second_fact_id>', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/init_facts_by_id.yaml', methods=['GET'])
def init_facts(first_fact_id, second_fact_id):
    return wrap_response(service.init_facts_endpoint(first_fact_id, second_fact_id))


@api_facts.route('/api/fact/<fact_id>', methods=['GET'])
@swag_from(f'{path}/docs/facts_docs/get_fact_by_id.yaml', methods=['GET'])
def get_fact(fact_id: str):
    return wrap_response(service.get_fact_endpoint(fact_id))


@api_facts.route('/api/fact/<fact_id>', methods=['DELETE'])
@swag_from(f'{path}/docs/facts_docs/del_fact_by_id.yaml', methods=['DELETE'])
def del_fact(fact_id: str):
    return wrap_response(service.delete_fact_endpoint(fact_id))
        
    

