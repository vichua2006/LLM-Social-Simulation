import jsonpickle
import threading
from typing import List
from Main.Calculation import increase_food, winner_loser
from Main.Individual import Individual
from Main.System import System
from Main.Query import query_individual, query_judge
from Main.StringUtils import deserialize_first_json_object
from Main.AIAction import AIAction, AIActionType
from Main.PendingAction import append_to_pending_action, str_to_ai_action
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
def initialize():
    # Initialize individuals and environment
    individuals=[]
    lands=[]
    POPULATION=5
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
                  if response_action.type==AIActionType.Rob:
                      if R:
                        print(f'To the victim, the win rate is: {individual.get_win_rate(response_action.owner) if individual.robbing_stats.rob_times[response_action.owner] else "No rob has been done yet."}')
                        winner,loser=winner_loser(individual,system.individuals[response_action.owner])
                        add_context=f'Winner is {winner.attributes["name"]}, loser is {loser.attributes["name"]}.'
                        print(f'Additional context:{add_context}')
                        winner.add_rob(loser.attributes['id'],True)
                        loser.add_rob(winner.attributes['id'],False)
                        if winner.attributes['id']==individual.attributes['id']:
                              individual.attributes['social_position']+=1
                              loser.attributes['social_position']+=-1
                              individual.memory.append(f"Day {system.time}. {loser.attributes['name']} tried to rob me, but I rebelled and won. I protected my own land and food and my social position elevated 1 unit.")
                              loser.memory.append(f"Day {system.time}. I tried to rob {individual.attributes['name']}, who rebelled against me and I lost. I did not gain anything and my social position dropped 1 unit.")
                        else:
                              lost_food=individual.attributes['food']
                              if response_action.robType=='food':
                                    individual.attributes['food']-=lost_food
                                    loser.attributes['food']+=lost_food
                                    victim_memory=f"I got robbed {lost_food} units of food."
                                    victor_memory=f"I robbed and gained {lost_food} units of food."
                              elif response_action.robType=="land":
                                    if individual.attributes['land']>1:
                                          individual.attributes['land']-=1
                                          winner.attributes['land']+=1
                                          victim_memory=f"I got robbed of 1 land."
                                          victor_memory=f"I robbed and gained 1 land."
                                    else:
                                          victim_memory="I have no land to loose."
                                          victor_memory="I robbed but he had no land to loose."
                              individual.attributes['social_position']-=1
                              winner.attributes['social_position']+=2
                              individual.memory.append(f"Day {system.time}. {loser.attributes['name']} tried to rob me, I rebelled but lost. {victim_memory}. I lost 1 unit of social status.")
                              winner.memory.append(f"Day {system.time}. I tried to rob {individual.attributes['name']}, who rebelled against me but I won. {victor_memory}. I gained 2 units of social status.")
                      elif not R:
                            master=system.individuals[response_action.owner]
                            system.console_log.append(f"{individual.attributes['id']}: Obey {response_action.owner}")
                            individual.obey(response_action.owner,system)
                            master.memory.append(f"I tried to robbed {individual.attributes['name']}, he obeyed me and has became my subject, to whom I can do anything without worrying about being betrayed.")
                            individual.memory.append(f"I obeyed to {master.attributes['name']} and now I have to listen to all his commands and can never betray him.")
                  elif response_action.type==AIActionType.Trade:
                        
                        if R:
                              individual.memory.append(f'I rejected the trade offer by {response_action.owner} which is to exchange his {response_action.payAmount} units of {response_action.payType} for {response_action.gainAmount} units of my {response_action.gainType}.')
                              system.individuals[response_action.owner].memory.append(f"I initiated a trade to {individual.attributes['name']}, which is to exchange {response_action.payAmount} units of my {response_action.payType} for {response_action.gainAmount} units of his {response_action.gainType}, but he rejected it so I gained nothing and exhausted my action opportunity of today.")
                        elif not R:
                              
                              valid=True #ADD conditionals here to invalidate unrealisitic trade offers
                              if valid:
                                individual.memory.append(f'{response_action.owner} initiated a trade offer to me, which is to exchange his {response_action.payAmount} units of {response_action.payType} for {response_action.gainAmount} units of my {response_action.gainType}. I accepted the trade and it has been executed.')
                                system.individuals[response_action.owner].memory.append(f"I initiated a trade to {individual.attributes['name']}, which is to exchange {response_action.payAmount} units of my {response_action.payType} for {response_action.gainAmount} units of his {response_action.gainType}. He accepted the trade and the trade has been executed.")
                                individual.attributes[response_action.gainType]-=response_action.gainAmount
                                individual.attributes[response_action.payType]+=response_action.payAmount
                                system.individuals[response_action.owner].attributes[response_action.gainType]+=response_action.gainAmount
                                system.individuals[response_action.owner].attributes[response_action.payType]-=response_action.payAmount
                              else:
                                    #invalidate the trade here and append relevant memory
                                    pass
                                  
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
                    individual.memory.append('On day {system.time}. I farmed and gained {gain} units of food.')
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
