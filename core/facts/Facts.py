from experta import Fact, Field

class Kebab(Fact):
    """
    Allowed variants
    """
    Meat = Field(list)
    Marinade = Field(str)
    Coal = Field(str)
    Woods = Field(str)
    Time = Field(int)
    Weather = Field(str)
    Fire = Field(str)
