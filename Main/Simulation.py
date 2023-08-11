import threading
import numpy as np
from typing import List
from Main.Individual import Individual, System
from Main.Query import query_individual, query_judge
from Main.StringUtils import deserialize_first_json_object
from Main.AIAction import AIAction, AIActionType
from Main.PendingAction import append_to_pending_action, str_to_ai_action

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
      for individual in individuals:
          if system.is_stop:
            print("Stop Simulation!")
            return
          index:int = individuals.index(individual)
          print(f"Person {index} is responding...\n")
          passive=not individual.pending_action.empty()
          if individual.attributes['action']>0 or passive:
            response_action = individual.pending_action.get() if not individual.pending_action.empty() else None
            action:str=query_individual(individual,system,response_action)
            if passive:
                  print(f'{individual.attributes["name"]} chooses to {action}')
                  individual.check_is_responser(response_action)
                  query_judge(f'In response to {response_action.owner} initiating {response_action}, {individual.attributes["name"]} chooses to {action}',individual,system)
            else:
              for o in range(5):
                if system.is_stop:
                  print("Stop Simulation!")
                  return
                try:
                  print("Action: "+action)
                  action = deserialize_first_json_object(action.lower())
                  ai_action:AIAction = str_to_ai_action(action, index)
                  individual.current_action_type = ai_action.type
                  append_to_pending_action(ai_action, system)
                  break
                except Exception as e:
                  try:
                    ai_action:AIAction = str_to_ai_action([action[x] for x in action][0], index)
                    append_to_pending_action(ai_action, system)
                    action=list(action[x] for x in action)[0]
                    break
                  except Exception as e2:print(f"First Exception:{e}, second exception:{e2}")
                  action:str=query_individual(individual,system,response_action)
              try:system.history.append(f'{individual.attributes["name"]}:{action["reason"]}')
              except:
                try:system.history.append(f'{individual.attributes["name"]}:{action[[x for x in action][0]]["reason"]}')
                except:system.history.append(f'{individual.attributes["name"]}:\n{action}')
              if action["action"]=="farm":
                    print("Farming identified.")
                    individual.attributes['food']+=np.random.uniform(0.9, 1.1)*individual.attributes["land"]/3
                    individual.attributes['action']=0
                    individual.memory.append(action['reason'])
              else:
                    individual.attributes['action']=0
                    individual.memory.append(action['reason'])
      system.ranking.update({x: x.attributes["social_position"] for x in system.individuals})
      print(f'OVERALL TRUST LEVEL:{sum([x.attributes["trust_of_others"] for x in system.individuals])}\n\n\n')
      #reach this mean all pending action is done
      pending=False
      for i in individuals:
            pending=pending or not i.pending_action.empty()
      if not pending:
        day_end(system,individuals)
        break
      else:
            print(f'Systme still pending actions, so will go into another round.')

