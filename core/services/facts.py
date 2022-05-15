import os

from core.config import logger
from core.models.Facts import Facts
from errors.exceptions import ExpertaBackendError


def get_all_facts_endpoint():
    try:
        return Facts.to_dict_list()
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return {'errors': ex.message}
    except Exception as e:
        # converting error to string
        error = repr(e)
        logger.error(error)
        return {'errors': {'message': error}}

def get_fact_endpoint(fact_id):
    try:
        return Facts.get_by_id(fact_id)
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return {'errors': ex.message}
    except Exception as e:
        # converting error to string
        error = repr(e)
        logger.error(error)
        return {'errors': {'message': error}}

def delete_fact_endpoint(fact_id):
    try:
        return Facts.delete_by_id(fact_id)
    except ExpertaBackendError as ex:
        logger.error(ex.message)
        return {'errors': ex.message}
    except Exception as e:
        # converting error to string
        error = repr(e)
        logger.error(error)
        return {'errors': {'message': error}}

def add_fact_endpoint(data):
    return Facts.add_new(data)

def init_fact_endpoint(fact_id):
    return Facts.init_fact_by_id(fact_id)

def init_facts_endpoint(first_fact_id, second_fact_id):
    return Facts.init_facts_by_id(first_fact_id, second_fact_id)
