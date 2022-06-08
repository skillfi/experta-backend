import os

from core.models.Facts import Facts
from errors.exceptions import AppBackendError


def get_all_facts_endpoint():
    return Facts.to_dict_list(Facts.get_list())


def get_fact_endpoint(fact_id):
    return Facts.get_by_id(rec_id=fact_id)


def delete_fact_endpoint(fact_id):
    return Facts.del_by_id(rec_id=fact_id)


def add_fact_endpoint(data):
    return Facts.add_new(data)


def init_fact_endpoint(fact_id):
    return Facts.init_fact_by_id(fact_id)


def init_facts_endpoint(first_fact_id, second_fact_id):
    return Facts.init_facts_by_id(first_fact_id, second_fact_id)
