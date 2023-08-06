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
  
      system.pending_action[(id,action["payload"]["tradepayload"]["targetid"])]=f'{action["action"]}:{action["payload"]["tradepayload"]["pay"]}:{action["payload"]["tradepayload"]["payamount"]}:{action["payload"]["tradepayload"]["gain"]}:{action["payload"]["tradepayload"]["gainamount"]}'
      print(f'Pending:{system.pending_action}')
    else:
      if(action["action"]=="rob"):
        if system.pending_action is None: system.pending_action={}
        system.pending_action[(id,action["payload"]["robpayload"]["targetid"])]=f'{action["action"]}:{action["payload"]["robpayload"]["robitem"]}'
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
    system.is_stop=False
    return system
  
def simulate(individuals:List[Individual],system:System):
    while True:
      for i in individuals:
          if system.is_stop:
            print("Stop Simulation!")
            return
          index:int = individuals.index(i)
          print(f"Person {index} is responding...\n")
          if i.attributes['action']>0 or get_related_pending_action(i,system):
            action:str=query_individual(i,system)
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
                print(f"Exception: {e}")
                action:str=query_individual(i,system)
            system.history.append(f'{i.attributes["name"]}:{action["reason"]}') 
            if action["action"]==AIAction.Farm:
                  print(f'Person {index} is farming...')
                  i.attributes['food']+=np.random.uniform(0.9, 1.1)*i.attributes["land"]/3
                  i.attributes['action']=0
                  i.memory.append(action['reason'])
            elif action["action"]==AIAction.Rob or action["action"]==AIAction.Trade:
                  print(f'Person {index} is robing or trading...')
                  i.attributes['action']=0
                  i.memory.append(action['reason'])
            else:
              query_judge(action, i,system)
      system.ranking.update({x: x.attributes["social_position"] for x in system.individuals})
      print(f'OVERALL TRUST LEVEL:{sum([x.attributes["trust_of_others"] for x in system.individuals])}\n\n\n')
      if not system.pending_action:
        break
      day_end(system,individuals)

