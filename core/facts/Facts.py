from experta import Fact, Field

class Kebab(Fact):
    """
    Allowed variants
    Meat: str ('Type 1','Type 2','Type 3')
    Action: str ('Action 1','Action 2','Action 3')
    Degree: str
    Part Done: str
    Time: int
    Turned Over: boolean
    Cooked For: str
    """
    Meat = Field(str)
    Action = Field(str)
    DegreeOfReadiness = Field(str)
    Pardone = Field(str)
    Time = Field(int)
    TurnedOver = Field(bool)
    CookedFor = Field(str)
