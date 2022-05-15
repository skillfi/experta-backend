import ast
from random import random, randrange, choice, choices

from core.config import logger
from core.models.Rule import Rule as Model
from core.tools import wrap_response
from errors.exceptions import ExpertaBackendError
from experta import (AND, AS, EXISTS, FORALL, MATCH, NOT, OR, TEST, DefFacts,
                     KnowledgeEngine, Rule)
from experta.fieldconstraint import L, P
from experta.utils import unfreeze_frozendict, unfreeze_frozenlist, unfreeze

from .Facts import Kebab as Fact


class System(KnowledgeEngine):

    response_object = dict(
        recomendation=str(),
        fact_id=str()
    )

    def init_fact(self, fact: dict, conditional: bool=None, length: int=None, data: list=None):
        if conditional:
            for i in range(0, length-1):
                obj = Fact(_id=str(data[i]['_id']),
                    Meat=data[i].get('Meat', []),
                    Marinade=data[i].get('Marinade', {}),
                    Coal=data[i].get('Coal'),
                    Woods=data[i].get('Woods'),
                    Fire=data[i].get('Fire'),
                    Weather=data[i].get('Weather'),
                    Time=data[i].get('Time')
                )
                facts = self.declare(obj)
        obj = Fact(_id=str(fact['_id']),
            Meat=fact.get('Meat'),
            Marinade=fact.get('Marinade'),
            Coal=fact.get('Coal', ''),
            Woods=fact.get('Woods', ''),
            Fire=fact.get('Fire', False),
            Weather=fact.get('Weather', ''),
            Time=fact.get('Time', 0)
        )
        facts = self.declare(obj)
        # return facts.as_dict()

    
    @Rule(AS.fact << Fact(Meat = MATCH.Meat))
    def _AS(self, Meat, fact):
        try:
            data = list()
            for rule in fact.as_dict()['Meat']:
                if rule == 'Шия':
                    self.response_object['fact_id'] = fact.get('_id')
                    self.response_object['recomendation'] =  f'{rule}: Вважається ідеальним вибором.'
                    data.append(self.response_object)
                if rule == 'Корейка':
                    self.response_object['fact_id'] = fact.get('_id')
                    self.response_object['recomendation'] = f'{rule}: Слід вибирати шматок з солідним вкрапленням сала, яке потопиться при смаженні й не дасть шашлику пересушитися.'
                    data.append(self.response_object)
                if rule == 'Вирізка':
                    self.response_object['fact_id'] = fact.get('_id')
                    self.response_object['recomendation'] = f'{rule}: Найм’якша частина з представлених, але після приготування такої шашлик бажано відразу подавати до столу.'
                    data.append(self.response_object)
            return Model.add_new(data, self)
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return {'errors': ex.message}
        except Exception as e:
            error = str(e)
            logger.error(error)
            resp = {
                'errors': {
                    'message': error
                }
            }
            return resp

    @Rule(OR(AS.fact << Fact(Fire=~L(False), Weather=MATCH.Weather),
            AS.fact << Fact(Fire=~L(True), Weather=MATCH.Weather)))
    def _OR(self, fact, Weather):
        try:
            data = list()
            for rule in fact.as_dict()['Weather']:
                if rule == 'Дощ' and fact.get('Fire'):
                    self.response_object['fact_id'] = fact.get('_id')
                    self.response_object['recomendation'] = f'Під час {rule}у не рекомендуємо робити шашлик в таку погоду!'
                    data.append(self.response_object)
                if rule == 'Сонячно' and not fact.get('Fire'):
                    self.response_object['fact_id'] = fact.get('_id')
                    self.response_object['recomendation'] = 'Погода не заважатиме пртготуванню шашлику!'
                    data.append(self.response_object)
            return Model.add_new(data, self)
            
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return wrap_response({'errors': ex.message})
        except Exception as e:
            error = str(e)
            logger.error(error)
            resp = {
                'errors': {
                    'message': error
                }
            }
            return wrap_response(resp)

    @Rule(AS.fact << Fact(Time=~L(P(lambda i: i>25))))
    def _L_P(self, fact):
        data = list()
        self.response_object['fact_id'] = fact.get('_id')
        self.response_object['recomendation'] = f'Шашлик ще не готовий. Потрібно не більше 20 хвилин на приготування'
        data.append(self.response_object)
        return Model.add_new(data, self)
        pass

    @Rule(
        EXISTS(
            Fact(
                Marinade=['Вино']
            )
        ))
    def _exist(self):
        try:
            fact = self.facts[1]
            data = list()
            self.response_object['fact_id'] = fact.get('_id')
            self.response_object['recomendation'] = f'Категорично заборонено використовувати заправки з кислим середовищем: {unfreeze_frozenlist(fact.get("Marinade"))}'
            data.append(self.response_object)
            return Model.add_new(data, self)
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return wrap_response({'errors': ex.message})
        except Exception as e:
            error = str(e)
            logger.error(error)
            resp = {
                'errors': {
                    'message': error
                }
            }
            return wrap_response(resp)
    
    @Rule(
        FORALL(
            Fact(Coal=['Слива']),
            Fact(Woods=['Тополя'])
        )
    )
    def _forall(self):
        try:
            fact = self.facts[1]
            data = list()
            self.response_object['fact_id'] = fact.get('_id')
            self.response_object['recomendation'] = f'На вуггіллі крім Сливи рекомендуємо на ваш вибір: Яблуня, Абрикоса. На сухому дереві окрім Тополі рекомендуємо: Клен, Дуб, Осика, Верба, Ліщини, Каштана, Липи'
            data.append(self.response_object)
            return Model.add_new(data, self)
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return wrap_response({'errors': ex.message})
        except Exception as e:
            error = str(e)
            logger.error(error)
            resp = {
                'errors': {
                    'message': error
                }
            }
            return wrap_response(resp)
    
    @Rule(
        AS.fact << Fact(
            Time=MATCH.Time, Coal=choice(['Слива', "Абрикоса", "Яблуня"]), Wood=choice(['Клен', "Дуб", "Тополя"])
        ),
        TEST(
            lambda Time: Time > 25
        )
    )
    def _test(self, Time, fact):
        try:
            data = list()
            self.response_object['fact_id'] = fact.get('_id')
            self.response_object['recomendation'] = f'Забагато часу: {Time}m. Шашлик перетвориться в вугілля'
            data.append(self.response_object)
            return Model.add_new(data, self)
        except ExpertaBackendError as ex:
            logger.error(ex.message)
            return wrap_response({'errors': ex.message})
        except Exception as e:
            error = str(e)
            logger.error(error)
            resp = {
                'errors': {
                    'message': error
                }
            }
            return wrap_response(resp)

