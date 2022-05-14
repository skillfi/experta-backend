import ast

from core.config import logger
from core.tools import wrap_response
from errors.exceptions import ExpertaBackendError
from experta import (AND, AS, EXISTS, FORALL, MATCH, NOT, OR, TEST, DefFacts,
                     KnowledgeEngine, Rule)
from experta.fieldconstraint import L, P

from .Facts import Kebab as Fact


class System(KnowledgeEngine):

    response_object = dict()

    def init_fact(self, fact: dict):
        obj = Fact(Meat=fact.get('Meat'),
            Action=fact.get('Action'),
            DegreeOfReadiness=fact.get('DegreeOfReadiness'),
            Pardone=fact.get('Pardone'),
            TurnedOver=fact.get('TurnedOver'),
            CookedFor=fact.get('CookedFor'),
            Time=fact.get('Time')
        )
        facts = self.declare(obj)
        return facts.as_dict()

    
    @Rule(AS.fact <<Fact(Meat='Курятина', Action='Перевернути'))
    def _AS(self, fact: dict):
        pass
        # try:
        #     # db = Mongo()
        #     # condi = {'Conditional': 'AS.fact << Fact()'}
        #     # fact.update(condi)
        #     # return db.add_new(fact,'Rules')
        # except ExpertaBackendError as ex:
        #     logger.error(ex.message)
        #     return wrap_response({'errors': ex.message}, True)
        # except Exception as e:
        #     error = str(e)
        #     logger.error(error)
        #     resp = {
        #         'errors': {
        #             'message': error
        #         }
        #     }
        #     return wrap_response(resp, True)
    

    @Rule(AND(Fact(),
            Fact()))
    def _AND():
        pass

    @Rule(OR(Fact(),
            Fact()))
    def _OR():
        pass

    @Rule(NOT(Fact()))
    def _Not():
        pass

