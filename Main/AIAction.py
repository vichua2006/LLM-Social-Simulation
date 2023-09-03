
from enum import Enum, EnumMeta
# Define a custom metaclass to handle string values for the enumeration
class StringEnumMeta(EnumMeta):
    def __call__(cls, value, *args, **kwargs):
        # If the value is a string, use it as the enumeration member
        if isinstance(value, str):
            try:
                return cls.__new__(cls, value)
            except ValueError:
                raise ValueError(f"{value} is not a valid {cls.__name__}")
        # Otherwise, fall back to the default behavior
        return super().__call__(value, *args, **kwargs)
    
# Define the string enum using the custom metaclass
class AIActionType(str, Enum, metaclass=StringEnumMeta):
    Default = "None"
    Farm = "farm"
    Rob = "rob"
    Trade = "trade"
    BeRobbed = "be robbed"
    BeTraded = "be traded"
    
#class Type(str, Enum, metaclass=StringEnumMeta):
 #   Land = "land"
  #  Food = "food"
   # Glory = "glory"
class AIAction:
    def __init__(self, type:AIActionType, owner:int, target:int) -> None:
        self.type:AIActionType = type
        self.owner:int = owner
        self.target:int = target
    def __str__(self) -> str:
        return f"{self.type}, owner: {self.owner}, target: {self.target}"
    
class RobAction(AIAction):
    def __init__(self, owner:int, target:int, robType:str) -> None:
        super().__init__(AIActionType.Rob, owner, target)
        self.robType:str= robType
    def __str__(self) -> str:
        return f"{self.type}, owner: {self.owner}, target: {self.target}, robType: {self.robType}"

        
class TradeAction(AIAction):
    def __init__(self, owner:int, target:int, payType:str, payAmount:float, gainType:str, gainAmount:float) -> None:
        super().__init__(AIActionType.Trade, owner, target)
        self.payType: str = payType
        self.payAmount: float = payAmount
        self.gainType: str = gainType
        self.gainAmount: float = gainAmount
    def __str__(self) -> str:
        return f"{self.type}, owner: {self.owner}, target: {self.target}, payType: {self.payType}, payAmount: {self.payAmount}, gainType: {self.gainType}, gainAmount: {self.gainAmount}" 
    