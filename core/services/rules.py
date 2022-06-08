from core.models.Rule import Rule


def get_all_rules_endpoint():
    return Rule.to_dict_list(Rule.get_list())


def get_rule_endpoint(rule_id):
    return Rule.get_by_id(rule_id)


def get_rule_by_fact_endpoint(fact_id):
    return Rule.to_dict_list(Rule.get_list_by_query({'fact_id':Rule.id(fact_id)}))


def delete_rule_endpoint(rule_id):
    return Rule.del_by_id(rule_id)

def delete_rules_by_fact_endpoint(fact_id):
    return Rule.del_by_fact_id(fact_id)
