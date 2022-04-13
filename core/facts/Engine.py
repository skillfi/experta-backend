import ast
from core.models.Mongo import Mongo
from core.config import logger
from core.tools import wrap_response
from errors.exceptions import ExpertaBackendError
from experta import (AND, AS, EXISTS, FORALL, MATCH, NOT, OR, TEST, DefFacts,
                     KnowledgeEngine, Rule)
from experta.fieldconstraint import L, P

from .Facts import Kebab as Fact


class System(KnowledgeEngine):
    def init_fact(self, post_data:dict, Turned: bool):
        try:
            obj = Fact(Meat=str(post_data.get('Meat')),
                Action=str(post_data.get('Action')),
                DegreeOfReadiness=str(post_data.get('DegreeOfReadiness')),
                Pardone=str(post_data.get('Pardone')),
                TurnedOver=Turned,
                CookedFor=post_data.get('CookedFor'),
                Time=int(post_data.get('Time'))
            )
            fact = self.declare(obj)
            db = Mongo()
            return db.add_new(fact.as_dict(), 'System')
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return wrap_response({'errors': ex.message}, True)
        except Exception as e:
            error = str(e)
            logger.error(error)
            resp = {
                'errors': {
                    'message': error
                }
            }
            return wrap_response(resp, True)

    
    @Rule(AS.fact <<Fact(Meat='Курятина', Action='Перевернути'))
    def _AS(self, fact: dict):
        try:
            db = Mongo()
            condi = {'Conditional': 'AS.fact << Fact()'}
            fact.update(condi)
            return db.add_new(fact,'Rules')
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return wrap_response({'errors': ex.message}, True)
        except Exception as e:
            error = str(e)
            logger.error(error)
            resp = {
                'errors': {
                    'message': error
                }
            }
            return wrap_response(resp, True)
    

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

