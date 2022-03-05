from experta import Fact, Field

class Kebab(Fact):
    Meat = Field(dict)
    Action = Field(str)
    DegreeOfReadiness = Field(dict)
    Time = Field(int)
    TurnedOver = Field(bool)
    CookedFor = Field(dict)

