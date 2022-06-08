from random import choice

from core.models.Rule import Rule as Model
from experta import (AND, AS, EXISTS, FORALL, MATCH, NOT, OR, TEST, DefFacts,
                     KnowledgeEngine, Rule)
from experta.fieldconstraint import L, P
from experta.utils import unfreeze, unfreeze_frozendict, unfreeze_frozenlist

from .Facts import Kebab as Fact


class System(KnowledgeEngine):

    response_object = dict(
        recommendation=str(),
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
        data = list()
        for rule in fact.as_dict()['Meat']:
            if rule == 'Шия':
                raw = dict(fact_id=fact.get('_id'), recommendation=f'{rule}: Вважається ідеальним вибором.')
                data.append(raw)
            elif rule == 'Корейка':
                raw = dict(fact_id=fact.get('_id'), recommendation=f'{rule}: Слід вибирати шматок з солідним вкрапленням сала, яке потопиться при смаженні й не дасть шашлику пересушитися.')
                data.append(raw)
            elif rule == 'Вирізка':
                raw = dict(fact_id=fact.get('_id'), recommendation=f'{rule}: Найм’якша частина з представлених, але після приготування такої шашлик бажано відразу подавати до столу.')
                data.append(raw)
        return Model.add_new(data)

    @Rule(OR(AS.fact << Fact(Fire=~L(False), Weather=MATCH.Weather),
            AS.fact << Fact(Fire=~L(True), Weather=MATCH.Weather)))
    def _OR(self, fact, Weather):
        data = list()
        for rule in fact.as_dict()['Weather']:
            if rule == 'Дощ' and fact.get('Fire'):
                self.response_object['fact_id'] = fact.get('_id')
                self.response_object['recommendation'] = f'Під час {rule}у не рекомендуємо робити шашлик в таку погоду!'
                data.append(self.response_object)
            elif rule == 'Сонячно' and not fact.get('Fire'):
                self.response_object['fact_id'] = fact.get('_id')
                self.response_object['recommendation'] = 'Погода не заважатиме пртготуванню шашлику!'
                data.append(self.response_object)
        return Model.add_new(data)

    @Rule(AS.fact << Fact(Time=~L(P(lambda i: i>25))))
    def _L_P(self, fact):
        data = list()
        self.response_object['fact_id'] = fact.get('_id')
        self.response_object['recommendation'] = f'Шашлик ще не готовий. Потрібно не більше 20 хвилин на приготування'
        data.append(self.response_object)
        return Model.add_new(data)
        pass

    @Rule(
        EXISTS(
            Fact(
                Marinade=['Вино']
            )
        ))
    def _exist(self):
        fact = self.facts[1]
        data = list()
        self.response_object['fact_id'] = fact.get('_id')
        self.response_object['recommendation'] = f'Категорично заборонено використовувати заправки з кислим середовищем: {unfreeze_frozenlist(fact.get("Marinade"))}'
        data.append(self.response_object)
        return Model.add_new(data)
    
    @Rule(
        FORALL(
            Fact(Coal=['Слива']),
            Fact(Woods=['Тополя'])
        )
    )
    def _forall(self):
        fact = self.facts[1]
        data = list()
        self.response_object['fact_id'] = fact.get('_id')
        self.response_object['recommendation'] = f'На вуггіллі крім Сливи рекомендуємо на ваш вибір: Яблуня, Абрикоса. На сухому дереві окрім Тополі рекомендуємо: Клен, Дуб, Осика, Верба, Ліщини, Каштана, Липи'
        data.append(self.response_object)
        return Model.add_new(data)
    
    @Rule(
        AS.fact << Fact(
            Time=MATCH.Time, Coal=choice(['Слива', "Абрикоса", "Яблуня"]), Wood=choice(['Клен', "Дуб", "Тополя"])
        ),
        TEST(
            lambda Time: Time > 25
        )
    )
    def _test(self, Time, fact):
        data = list()
        self.response_object['fact_id'] = fact.get('_id')
        self.response_object['recommendation'] = f'Забагато часу: {Time}m. Шашлик перетвориться в вугілля'
        data.append(self.response_object)
        return Model.add_new(data)

