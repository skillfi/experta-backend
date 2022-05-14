import os

import core.services.rules as service
from core.tools import wrap_response
from flasgger import swag_from
from flask import Blueprint, request

api_rules = Blueprint('api_rules', __name__)
path = os.getcwd()

@api_rules.route('/api/rules', methods=['GET'])
@swag_from(f'{path}/docs/rules_docs/get_all_rules.yaml')
def get_facts_list():
    return wrap_response(service.get_all_rules_endpoint())

@api_rules.route('/api/rule/<rule_id>', methods=['GET'])
@swag_from(f'{path}/docs/rules_docs/get_rule_by_id.yaml')
def get_rule_by_id(rule_id):
    return wrap_response(service.get_rule_endpoint(rule_id))
