from typing import List
from Main.AIAction import AIAction, AIActionType, RobAction, TradeAction
from Main.System import System

def str_to_ai_action(action:str, id:int)->AIAction:
    if(action["action"]=="trade"):
      return TradeAction(id, action["payload"]["tradepayload"]["targetid"], action["payload"]["tradepayload"]["paytype"], action["payload"]["tradepayload"]["payamount"], action["payload"]["tradepayload"]["gaintype"], action["payload"]["tradepayload"]["gainamount"])
    elif action["action"]=="rob":
      return RobAction(id, action["payload"]["robpayload"]["targetid"], action["payload"]["robpayload"]["robtype"])
    elif action["action"]=='farm':
          return AIAction(AIActionType.Farm,id,None)
    else:print("Error: Invalid action type")
      
def append_to_pending_action(action:AIAction, system:System)->None:
    id:int = action.target
    system.individuals[id].pending_action.put(action)