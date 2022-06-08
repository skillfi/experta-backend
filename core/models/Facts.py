from datetime import datetime

from bson.objectid import ObjectId
from core.config import config, db, logger
from core.facts.Engine import System
from core.models.base.DbModelBase import DbModelBase
from core.tools import wrap_response
from errors.exceptions import AppBackendError, UnknownIdError
from pymongo.errors import PyMongoError

engine = System()
engine.reset()

class Facts(DbModelBase):
    """Facts Model for Storing facts related details"""
    __tablename__ = db.System

    def __init__(self, Meat, Marinade, Coal, Woods, Fire, Weather, Time) -> 'Facts':
        self.Meat = Meat
        self.Marinade = Marinade
        self.Coal = Coal
        self.Woods = Woods
        self.Fire = Fire
        self.Weather = Weather
        self.Time = Time
        self.update_time = datetime.now().strftime(config['DATETIME_FORMAT'])
        # self._id = str(uuid.uuid4())
    
    @property
    def FireBool(self):
        if self.Fire == 'true':
            self.Fire = True
            return self.__dict__
        else:
            self.Fire = False
            return self.__dict__

    @staticmethod
    def add_new(post_data: dict) -> 'dict':
        """
        Add new Fact

        :param dict post_data: Dictionary
        """
        try:
            if isinstance(post_data.get('Time'), str) and post_data.get('Time') != '':
                post_data['Time'] = int(post_data['Time'])
            if isinstance(post_data.get('Time'), str) and post_data.get('Time') == '':
                post_data['Time'] = 0
            fact = Facts(
                Meat=post_data.get('Meat'),
                Marinade=post_data.get('Marinade'),
                Coal=post_data.get('Coal'),
                Woods=post_data.get('Woods'),
                Fire=post_data.get('Fire', True),
                Weather=post_data.get('Weather'),
                Time=post_data.get('Time', 0)
            )
            result = fact.__tablename__.insert_one(fact.FireBool)
            return Facts.get_by_id(str(result.inserted_id))
        except PyMongoError as ex:
            raise AppBackendError(ex)

    @staticmethod
    def init_fact_by_id(fact_id) -> 'dict':
        fact_to_rules = Facts.__tablename__.find_one(Facts.id(fact_id))
        engine.init_fact(fact_to_rules)
        engine.run()
    
    @staticmethod
    def init_facts_by_id(first_fact_id, second_fact_id) -> 'dict':
        facts = []
        fact_to_rules = Facts.__tablename__.find_one(Facts.id(first_fact_id))
        second_fact_to_rules = Facts.__tablename__.find_one(Facts.id(second_fact_id))
        facts.append(fact_to_rules)
        facts.append(second_fact_to_rules)
        engine.init_fact(fact_to_rules, True, len(facts), facts)
        return engine.run()

