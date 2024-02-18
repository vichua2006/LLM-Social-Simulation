from typing import List
from Main.AIAction import AIAction, AIActionType, DonateAction, RobAction, TradeAction
from Main.System import System
from Main.Individual import Individual

def str_to_ai_action(action:int, id:int)->AIAction:
    if(action["action"] == "trade"):
      return TradeAction(id, action["payload"]["targetid"], action["payload"]["paytype"], action["payload"]["payamount"], action["payload"]["gaintype"], action["payload"]["gainamount"])
    elif action["action"] == "rob":
      return RobAction(id, action["payload"]["targetid"], action["payload"]["robtype"])
    elif action["action"] == "farm":
     return AIAction(AIActionType.Farm,id,None)
    elif action["action"] == "produce":
      return AIAction(AIActionType.ProduceLuxury, id, None)
    elif action["action"] == "donate":
      return DonateAction(id, action["payload"]["targetid"], action["payload"]["donatetype"])
    else:print("Error: Invalid action type")
    return None
      
def append_to_pending_action(action:AIAction, system:System)->None:
    id:int = action.targetid
    person:Individual = next((person for person in system.individuals if person.attributes["id"] == id), None)
    person.pending_action.put(action)