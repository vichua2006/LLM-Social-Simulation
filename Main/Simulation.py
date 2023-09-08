import jsonpickle
import threading
from typing import List
from Main.Calculation import increase_food, rob, winner_loser
from Main.Individual import Individual
from Main.System import System
from Main.Query import query_individual
from Main.StringUtils import deserialize_first_json_object
from Main.AIAction import AIAction, AIActionType
from Main.PendingAction import append_to_pending_action, str_to_ai_action
from Main.SaveLoad import save_logframes, init_save

import random


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
        # Limit the memory to the last 60 events
        forget = len(individual.memory) - 60
        individual.memory = individual.memory[forget:]
    system.time+=1
    save_logframes(system)
  
def initialize():
    # Initialize individuals and environment
    individuals=[]
    lands=[]
    POPULATION=5
    #POPULATIONLIST=[x for x in range(POPULATION)]
    #random id
    #random_numbers = random.sample(POPULATIONLIST, POPULATION)
    #for i in random_numbers:
      #individuals.append(Individual(i,f'person {i}'))
      #lands.append(f'land {i}')
    #individuals.sort(key=lambda x: x.attributes['id'])
    #default
    for i in range(POPULATION):
      individuals.append(Individual(i,f'person {i}'))
      lands.append(f'land {i}')
    system=System(individuals,lands)
    init_save(system)
    return system

def simulate(individuals:List[Individual],system:System):
    while True:
      for individual in individuals:
          if system.is_stop:
            print("Stop Simulation!")
            return
          index:int = individuals.index(individual)
          passive=not individual.pending_action.empty()
          if individual.attributes['action']>0 or passive:
            print(f"Person {index} is responding...\n")
            response_action: AIAction = individual.pending_action.get() if not individual.pending_action.empty() else None
            action:str=query_individual(individual,system,response_action)
            if passive:
                  print(f'{individual.attributes["name"]} chooses to {action}')
                  individual.check_is_responser(response_action)
                  add_context=''
                  R=action[0]=="R"
                  owner:Individual=system.individuals[response_action.ownerid]
                  if response_action.type==AIActionType.Rob:
                      if R:
                        rob(individual, owner, system, response_action.robType)
                      elif not R:
                            if system.individuals[response_action.ownerid].attributes["id"] !=  individual.obey_stats.obey_personId:
                              master=system.individuals[response_action.ownerid]
                              master.add_rob(individual.attributes['id'],True)
                              system.console_log.append(f"{individual.attributes['id']}: Obey {response_action.ownerid}")
                              individual.obey(response_action.ownerid,system)
                              master.memory.append(f"I tried to robbed {individual.attributes['name']}, he obeyed me and has became my subject, to whom I can do anything without worrying about being betrayed.")
                              individual.memory.append(f"I obeyed to {master.attributes['name']} and now I have to listen to all his commands and can never betray him.")
                            else:
                              master=system.individuals[response_action.ownerid]
                              master.add_rob(individual.attributes['id'],True)
                              system.console_log.append(f"{individual.attributes['id']}: Accept robbery from {response_action.ownerid}")
                              print("success accepting robbery from master")
                  elif response_action.type==AIActionType.Trade:
                        owner.memory.append(f"Day {system.time}. I initiated a trade to {individual.attributes['name']}, which is to exchange {response_action.payAmount} units of my {response_action.payType} for {response_action.gainAmount} units of his {response_action.gainType}.")
                        individual.memory.append(f"Day {system.time}.{response_action.ownerid} initiated a trade offer to me, which is to exchange his {response_action.payAmount} units of {response_action.payType} for {response_action.gainAmount} units of my {response_action.gainType}. ")
                        if R:
                              individual.memory.append(f'I rejected the trade offer by {response_action.ownerid}.')
                              system.individuals[response_action.ownerid].memory.append(f"But he rejected it so I gained nothing and exhausted my action opportunity of today.")
                        elif not R:
                              owner=system.individuals[response_action.ownerid]
                              gainT=response_action.gainType
                              gainA=response_action.gainAmount
                              payA=response_action.payAmount
                              payT=response_action.payType
                              validO=owner.attributes[payT]>=payA
                              validI=individual.attributes[gainT]>=gainA#ADD conditionals here to invalidate unrealisitic trade offers
                              if validO and validI:
                                individual.memory.append(f'I accepted the trade and it has been executed.')
                                owner.memory.append("He accepted the trade and the trade has been executed.")
                                individual.attributes[gainT]-=gainA
                                individual.attributes[payT]+=payA
                                owner.attributes[gainT]+=gainA
                                owner.attributes[payT]-=payA
                              else:
                                if not validO:
                                      owner.memory.append("He accepted the trade but it couldn't go through since I don't have enough resource for it, and I got nothing out of this trade while I lost my action opportunity of today.")
                                      individual.memory.append("I accepted the trade but it couldn't go through because he doesn't have enough resources to pay me accordingly.")
                                if not validI:
                                      owner.memory.append("He accepted the trade but it could't go through because he didn't have enough resources to pay me accordingly. I lost my action opportunity of today.")
                                      individual.memory.append("I accepted the trade but I don't have enough resources to pay him accordingly so it failed to execute.")
                            
                                  
                  #query_judge(f'In response to Person {response_action.owner} initiating {response_action}, {individual.attributes["name"]} chooses to {action}. {add_context}',response_action,individual,system)
            elif not passive:
              for o in range(5):
                print(action)
                if system.is_stop:
                  print("Stop Simulation!")
                  return
                try:
                  action = deserialize_first_json_object(action.lower())
                  ai_action:AIAction = str_to_ai_action(action, index)
                  break
                except Exception as e:
                  try:
                    ai_action:AIAction = str_to_ai_action([action[x] for x in action][0], index)
                    action=list(action[x] for x in action)[0]
                    break
                  except Exception as e2:
                    print(f"First Exception:{e}, second exception:{e2}")
                    action:str=query_individual(individual,system,response_action)
                    continue
              individual.current_action_type = ai_action.type
              if ai_action.type==AIActionType.Farm:
                    land=individual.attributes['land']
                    gain=land*random.random()*0.3 if land>1 else 1
                    individual.attributes['food']+=gain
                    individual.memory.append(f'On day {system.time}. I farmed and gained {gain} units of food.')
                    print("Farm is successful.")
              elif ai_action.type==AIActionType.Rob or ai_action.type==AIActionType.Trade:
                    append_to_pending_action(ai_action, system)
                    print("Result yet to be seen.")
              else:
                    print(f'Problem, the type of the action is:{ai_action.type}')
              try:system.history.append(f'{individual.attributes["name"]}:{action["reason"]}')
              except:
                try:system.history.append(f'{individual.attributes["name"]}:{action[[x for x in action][0]]["reason"]}')
                except:system.history.append(f'{individual.attributes["name"]}:\n{action}')
                
              match individual.current_action_type:
                case AIActionType.Farm:
                  system.console_log.append(f"{index}:🌾")
                  increase_food(individual)
                case AIActionType.Trade:
                  system.console_log.append(f"{index}:🤝")
                case AIActionType.Rob:
                  system.console_log.append(f"{index}:🗡️")
                case AIActionType.BeRobbed:
                  system.console_log.append(f"{index}:🛡️")
                case _ :
                  system.console_log.append(f"{index}:Error")
              individual.attributes['action']-=1
              
      system.ranking.update({x: x.attributes["social_position"] for x in system.individuals})
      print(f'OVERALL TRUST LEVEL:{sum([x.attributes["trust_of_others"] for x in system.individuals])}\n\n\n')
      #reach this mean all pending action is done
      pending=False
      for i in individuals:
            pending=pending or not i.pending_action.empty()
      if not pending:
        break
      else:
            print(f'System still pending actions, so will go into another round.')
    day_end(system,individuals)

# %%
