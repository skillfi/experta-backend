from experta import Fact, Field

class Kebab(Fact):
    """
    Allowed variants
    """
    _id = Field(str)
    Meat = Field(list, default=[])
    Marinade = Field(list, default=[])
    Coal = Field(list, default=[])
    Woods = Field(list, default=[])
    Time = Field(int, default=0)
    Weather = Field(list, default=[])
    Fire = Field(bool, default='')
