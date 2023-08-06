from typing import List
from Main.Individual import Individual, System
def get_related_pending_action(individual:Individual,system:System):
    pending:List[str] =[]
    for i in system.pending_action:
        #if receiver is the individual, then add the pending action to the list
        if i[1]==individual.attributes["id"]:
          pending.append(f'Person {i[0]} initiated {system.pending_action[i]}')
    print("get_related_pending_action", pending)
    return pending
