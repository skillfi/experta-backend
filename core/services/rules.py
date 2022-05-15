import os

from core.config import logger
from core.models.Rule import Rule
from errors.exceptions import ExpertaBackendError


def get_all_rules_endpoint():
    try:
        return Rule.to_dict_list()
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return {'errors': ex.message}
    except Exception as e:
        # converting error to string
        error = repr(e)
        logger.error(error)
        return {'errors': {'message': error}}

def get_rule_endpoint(rule_id):
    try:
        return Rule.get_by_id(rule_id)
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return {'errors': ex.message}
    except Exception as e:
        # converting error to string
        error = repr(e)
        logger.error(error)
        return {'errors': {'message': error}}

def get_rule_by_fact_endpoint(fact_id):
    try:
        return Rule.get_by_fact_id(fact_id)
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return {'errors': ex.message}
    except Exception as e:
        # converting error to string
        error = repr(e)
        logger.error(error)
        return {'errors': {'message': error}}

def delete_rule_endpoint(rule_id):
    try:
        return Rule.delete_by_id(rule_id)
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return {'errors': ex.message}
    except Exception as e:
        # converting error to string
        error = repr(e)
        logger.error(error)
        return {'errors': {'message': error}}