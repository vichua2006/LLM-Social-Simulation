from typing import List
from Main.AIAction import AIAction, AIActionType, DonateAction, RobAction, TradeAction, ConsumeAction
from Main.System import System
from Main.Individual import Individual

def str_to_ai_action(action:str, id:int)->AIAction:
    if(action["action"]=="trade"):
      return TradeAction(id, action["payload"]["tradepayload"]["targetid"], action["payload"]["tradepayload"]["paytype"], action["payload"]["tradepayload"]["payamount"], action["payload"]["tradepayload"]["gaintype"], action["payload"]["tradepayload"]["gainamount"])
    elif action["action"]=="rob":
      return RobAction(id, action["payload"]["robpayload"]["targetid"], action["payload"]["robpayload"]["robtype"])
    elif action["action"]=='farm':
     return AIAction(AIActionType.Farm,id,None)
    elif action["action"] == "produce_luxury_good":
       return AIAction(AIActionType.ProduceLuxury, id, None)
    elif action["action"] == "consume_luxury_good":
       return ConsumeAction(id, None, action["payload"]["consumepayload"]["amount"])
    elif action["action"] == "donate":
      return DonateAction(id, action["payload"]["donatepayload"]["targetid"], action["payload"]["donatepayload"]["donatetype"])
    else:print("Error: Invalid action type")
      
def append_to_pending_action(action:AIAction, system:System)->None:
    id:int = action.targetid
    person:Individual = system.individuals[id]
    person.pending_action.put(action)