
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
class AIAction(str, Enum, metaclass=StringEnumMeta):
    Default = "None"
    Farm = "farm"
    Rob = "rob"
    Trade = "trade"
    BeRobbed = "be robbed"
    BeTraded = "be traded"

#class Item(str, Enum, metaclass=StringEnumMeta):
 #   Land = "land"
  #  Food = "food"
   # Glory = "glory"
class PendingAction:
    def __init__(self, type:AIAction) -> None:
        self.type:AIAction = type
class RobAction(PendingAction):
    def __init__(self, robItem:str) -> None:
        super().__init__(AIAction.Rob)
        self.robItem:str= robItem
        
class TradeAction(PendingAction):
    def __init__(self, payItem:str, payAmount:float, gainItem:str, gainAmount:float) -> None:
        super().__init__(AIAction.Trade)
        self.payItem: str = payItem
        self.payAmount: float = payAmount
        self.gainItem: str = gainItem
        self.gainAmount: float = gainAmount