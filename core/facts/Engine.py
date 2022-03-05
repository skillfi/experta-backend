import ast
from core.models.Mongo import Mongo
from core.tools import wrap_response
from errors.exceptions import ExpertaBackendError
from experta import (AND, AS, EXISTS, FORALL, MATCH, NOT, OR, TEST, DefFacts,
                     KnowledgeEngine, Rule)
from experta.fieldconstraint import L, P

from .Facts import Kebab as Fact


class System(KnowledgeEngine):
    def init_fact(self, post_data:dict, Turned: bool):
        try:
            obj = Fact(Meat=ast.literal_eval(post_data.get('Meat')),
                Action=post_data.get('Action'),
                DegreeOfReadiness=ast.literal_eval(post_data.get('DegreeOfReadiness')),
                TurnedOver=Turned,
                CookedFor=ast.literal_eval(post_data.get('CookedFor')),
                Time=int(post_data.get('Time'))
            )
            fact = self.declare(obj)
            db = Mongo()
            return db.add_new(fact.as_dict(), 'System')
        except ExpertaBackendError as ex:
            # logger.error(ex.message)
            return wrap_response({'errors': ex.message}, True)
        except Exception as e:
            error = str(e)
            # logger.error(error)
            resp = {
                'errors': {
                    'message': error
                }
            }
            return wrap_response(resp, True)

    
    @Rule(AND(Fact(Meat=MATCH.Meat), AS.fact <<Fact()))
    def check_conditions(self, Meat, fact):
        pass
