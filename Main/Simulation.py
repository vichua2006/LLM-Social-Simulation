import threading
import numpy as np
from typing import List
from Main.Individual import Individual, System
from Main.Query import query_individual, query_judge
from Main.StringUtils import deserialize_first_json_object
from Main.AIAction import AIAction
from Main.PendingAction import get_related_pending_action
#Noted that action is all lower case
def append_to_pending_action(id:int, action, system:System):
    if(action["action"]=="trade"):
      if system.pending_action is None: system.pending_action={}
  
      system.pending_action[(id,action["payload"]["tradepayload"]["targetid"])]=f'''Person {id} proposes to trade {action["payload"]["tradepayload"]["payamount"]} {action["payload"]["tradepayload"]["pay"]} for Person {action["payload"]["tradepayload"]["targetid"]}'s {action["payload"]["tradepayload"]["gainamount"]} {action["payload"]["tradepayload"]["gain"]}'''
      print(f'Pending action being added:{system.pending_action}')
    else:
      if(action["action"]=="rob"):
        if system.pending_action is None: system.pending_action={}
        system.pending_action[(id,action["payload"]["robpayload"]["targetid"])]=f'{action["action"]} against {action["payload"]["robpayload"]["targetid"]} for more {action["payload"]["robpayload"]["robitem"]}'
        print(f'Pending:{system.pending_action}')
      else:
        print("System: No pending action need to be added")
        
def change_affected_people(affected_people, system:System):
    for affected_person in affected_people:#{PERSON:{strength:1,...}...}
    #avoid if affected_person is "person 0" instead of "0"
      affected_person_index = int(affected_person.replace("person", "").replace(" ", ""))
      for attribute in affected_people[affected_person]:
        system.individuals[affected_person_index].attributes[attribute]=affected_people[affected_person][attribute]
        
# %%
# Function to update the state of each individual at the end of the day
def day_end(system,individuals:List[Individual]):
    for individual in individuals:
        if individual.attributes['food'] >= 1:
            individual.attributes['food'] -= 1  # Decrease the food by 1
        individual.attributes['action'] += 1  # Increase the action points by 1
        # Limit the memory to the last 30 events
        forget = len(individual.memory) - 40
        individual.memory = individual.memory[forget:]
        system.time+=1
def initialize():
    # Initialize individuals and environment
    individuals=[]
    lands=[]
    POPULATION=9
    for i in range(POPULATION):
      individuals.append(Individual(i,f'person {i}'))
      lands.append(f'land {i}')
    system=System(individuals,lands)
    return system
  
def simulate(individuals:List[Individual],system:System):
    while True:
      for i in individuals:
          if system.is_stop:
            print("Stop Simulation!")
            return
          index:int = individuals.index(i)
          pending=get_related_pending_action(i,system)
          print(f"Person {index} is responding...\n")
          if i.attributes['action']>0 or pending:
            action:str=query_individual(i,system)
            if pending:
              query_judge(action, i,system)
            else:
              for o in range(5):
                if system.is_stop:
                  print("Stop Simulation!")
                  return
                try:
                  print("Action: "+action)
                  action = deserialize_first_json_object(action.lower())
                  append_to_pending_action(index, action, system)
                  break
                except Exception as e:
                  try:
                    append_to_pending_action(index, [action[x] for x in action][0], system)
                    action=list(action[x] for x in action)[0]
                    break
                  except Exception as e2:print(f"First Exception:{e}, second exception:{e2}")
                  action:str=query_individual(i,system)
              try:system.history.append(f'{i.attributes["name"]}:{action["reason"]}')
              except:
                try:system.history.append(f'{i.attributes["name"]}:{action[[x for x in action][0]]["reason"]}')
                except:system.history.append(f'{i.attributes["name"]}:\n{action}')
              if action["action"]==AIAction.Farm:
                    i.attributes['food']+=np.random.uniform(0.9, 1.1)*i.attributes["land"]/3
                    i.attributes['action']=0
                    i.memory.append(action['reason'])
              elif action["action"]==AIAction.Rob or action["action"]==AIAction.Trade:
                    i.attributes['action']=0
                    i.memory.append(action['reason'])
      system.ranking.update({x: x.attributes["social_position"] for x in system.individuals})
      print(f'OVERALL TRUST LEVEL:{sum([x.attributes["trust_of_others"] for x in system.individuals])}\n\n\n')
      if not system.pending_action:
        day_end(system,individuals)
        break

