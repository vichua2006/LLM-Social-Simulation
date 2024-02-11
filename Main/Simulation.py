import os
import json
from typing import List
from Main.Calculation import donate, increase_food, punishment, rob_rebelled, winner_loser
from Main.CsvAnalysis import CsvAnalysis
from Main.Individual import Individual
from Main.System import System
from Main.Query import query_individual
from Main.StringUtils import deserialize_first_json_object
from Main.AIAction import AIAction, AIActionType
from Main.PendingAction import append_to_pending_action, str_to_ai_action
from Main.SaveLoad import init_save, save_logframes
from Main.Memory import ConceptNode
from Main.Conversation import converse, add_memory_after_conversation
import random
import datetime


csv_file_name='Log/'+datetime.datetime.now().strftime("%d, %I %M%p")+'.csv'
#if file name alread exist, datetime will be as detail as second
if os.path.exists(csv_file_name):
    csv_file_name='Log/'+datetime.datetime.now().strftime("%d, %I %M %S%p")+'.csv'

conversation_dir = f"conversation_and_memory_log/{datetime.datetime.now().strftime('%d, %I %M %S%p')}/"

# number of days between conversations
days_between_conversation = 1

def discuss_topic(system: System, individuals: List[Individual], topic: str, day_count: int):
  '''
  Initiate a conversation between individuals on a topic for discussion. 
  Their memories are updated afterwards with the contents of the conversation from their own perspective.
  '''

  # let agents converse
  conversation = converse(individuals, system, topic)
  # update the memory of each agent afterward
  add_memory_after_conversation(individuals, conversation)

  # record store the conversation and generated memories as text files to be later analysed

  memories = []
  for person in individuals:
    memories.append(person.memorystream.concept_nodes[-1].description)
  
  if not (os.path.exists(conversation_dir)):
    os.mkdir(conversation_dir)
  
  with open(f"{conversation_dir}day_{day_count}_conversation.txt", "w") as f:
    f.write(json.dumps(conversation, indent=4))
  with open(f"{conversation_dir}day_{day_count}_memory.txt", "w") as f:
    for memory in memories:
      f.write(memory)
      f.write("\n")
  
  return
  


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
    if system.day_end_counter > 0:
        system.day_end_counter += 1
    if system.day_end_counter > 10:
        system.should_exit = True

def initialize():
    # Initialize individuals and environment
    individuals=[]
    lands=[]
    POPULATION=3
    #POPULATIONLIST=[x for x in range(POPULATION)]
    #random id
    #random_numbers = random.sample(POPULATIONLIST, POPULATION)
    #for i in random_numbers:
      #individuals.append(Individual(i,f'person {i}'))
      #lands.append(f'land {i}')
    #individuals.sort(key=lambda x: x.attributes['id'])
    #default
    for i in range(POPULATION):
      individual = Individual(i,f'person_{i}')
      individuals.append(individual)
      lands.append(f'land {i}')
    system=System(individuals,lands)
    # init_save(system)
    system.set_csv_analysis(CsvAnalysis(POPULATION, csv_file_name))
    return system


def simulate(individuals:List[Individual],system:System):
    while True:
      for individual in individuals:
          if system.is_stop:
            print("Stop Simulation!")
            return
          index:int = individuals.index(individual)
          passive=not individual.pending_action.empty()
          if individual.attributes['action']>0 or not individual.pending_action.empty():
            passive=not individual.pending_action.empty()
            print(f"Person {index} is responding...\n")
            response_action: AIAction = individual.pending_action.get() if passive else None
            print(response_action)
            action:str=query_individual(individual,system,response_action)
            
            if passive and response_action is not None:
                  print(f'{individual.attributes["name"]} chooses to {action}')
                  individual.check_is_responser(response_action)
                  # add_context=''
                  R=action[0]=="R"
                  owner:Individual=system.individuals[response_action.ownerid]
                  if response_action.type==AIActionType.Rob:
                      
                      #if subject rob subject, this rob will be prohibited and the master will punish the subject and share the gain with all other subjects
                      if owner.obey_stats.obey_personId==individual.obey_stats.obey_personId and owner.obey_stats.obey_personId != -1:
                        print("DETECT: subject rob subject, pushiment will be given.")
                        punishment(owner, system)
                      
                      elif R:
                        rob_rebelled(individual, owner, system, response_action.robType)
                        system.csv_analysis.rob_rebelled(owner.attributes["id"])
                      elif not R:
                            #if master rob subject, subject will accept instead of obey, where obey only refer to the first obey that happen between two individuals without subject-master relationship
                            if owner.attributes["id"] !=  individual.obey_stats.obey_personId:
                              owner.add_rob(individual.attributes['id'],True)
                              system.console_log.append(f"{individual.attributes['id']}: Obey {response_action.ownerid}")
                              individual.obey(response_action.ownerid,system)
                              obey_node = ConceptNode(len(owner.memorystream.concept_nodes),"obey", system.time, owner.attributes["id"], "is obbeyed by", [individual.attributes["id"]], 0, f"I tried to robbed {individual.attributes['name']}, he obeyed me and has became my subject, to whom I can do anything without worrying about being betrayed.", 1)
                              owner.memorystream.add_concept_node(obey_node)
                              owner.memory.append(f"I tried to robbed {individual.attributes['name']}, he obeyed me and has became my subject, to whom I can do anything without worrying about being betrayed.")
                              obeyTo_node = ConceptNode(len(individual.memorystream.concept_nodes), "obey", system.time, owner.attributes["id"], "obey to", [individual.attributes["id"]], 0, f"I obeyed to {owner.attributes['name']} and now I have to listen to all his commands and can never betray him.", 1)
                              individual.memorystream.add_concept_node(obeyTo_node)
                              individual.memory.append(f"I obeyed to {owner.attributes['name']} and now I have to listen to all his commands and can never betray him.")
                              system.csv_analysis.obey(system)
                            else:
                              owner =system.individuals[response_action.ownerid]
                              owner.add_rob(individual.attributes['id'],True)
                              system.console_log.append(f"{individual.attributes['id']}: Accept robbery from {response_action.ownerid}")
                              print("success accepting robbery from master")
                  elif response_action.type==AIActionType.Trade:
                        trade_node = ConceptNode(len(owner.memorystream.concept_nodes), "trade", system.time, owner.attributes["id"], "trade with", [individual.attributes["id"]], 0, f"Day {system.time}. I initiated a trade to {individual.attributes['name']}, which is to exchange {response_action.payAmount} units of my {response_action.payType} for {response_action.gainAmount} units of his {response_action.gainType}.", 1)
                        owner.memorystream.add_concept_node(trade_node)
                        owner.memory.append(f"Day {system.time}. I initiated a trade to {individual.attributes['name']}, which is to exchange {response_action.payAmount} units of my {response_action.payType} for {response_action.gainAmount} units of his {response_action.gainType}.")
                        trade_node_ = ConceptNode(len(individual.memorystream.concept_nodes), "trade", system.time, owner.attributes["id"], "trade with", [individual.attributes["id"]], 0, f"Day {system.time}.{response_action.ownerid} initiated a trade offer to me, which is to exchange his {response_action.payAmount} units of {response_action.payType} for {response_action.gainAmount} units of my {response_action.gainType}. ", 1)
                        individual.memorystream.add_concept_node(trade_node_)
                        individual.memory.append(f"Day {system.time}.{response_action.ownerid} initiated a trade offer to me, which is to exchange his {response_action.payAmount} units of {response_action.payType} for {response_action.gainAmount} units of my {response_action.gainType}. ")
                        
                        if R:
                              no_trade_node = ConceptNode(len(owner.memorystream.concept_nodes), "trade", system.time, owner.attributes["id"], "trade with", [individual.attributes["id"]], 0, f'I rejected the trade offer by {response_action.ownerid}.', 1)
                              individual.memorystream.add_concept_node(no_trade_node)
                              individual.memory.append(f'I rejected the trade offer by {response_action.ownerid}.')
                              no_trade_node_ = ConceptNode(len(individual.memorystream.concept_nodes), "trade", system.time, owner.attributes["id"], "trade with", [individual.attributes["id"]], 0, f"But he rejected it so I gained nothing and exhausted my action opportunity of today.", 1)
                              owner.memorystream.add_concept_node(no_trade_node_)
                              owner.memory.append(f"But he rejected it so I gained nothing and exhausted my action opportunity of today.")
                        elif not R:
                              gainT=response_action.gainType
                              gainA=response_action.gainAmount
                              payA=response_action.payAmount
                              payT=response_action.payType
                              validO=owner.attributes[payT]>=payA
                              validI=individual.attributes[gainT]>=gainA#ADD conditionals here to invalidate unrealisitic trade offers
                              if validO and validI:
                                yes_trade_node = ConceptNode(len(owner.memorystream.concept_nodes), "trade", system.time, owner.attributes["id"], "trade with", [individual.attributes["id"]], 0, f'I accepted the trade and it has been executed.', 1)
                                individual.memorystream.add_concept_node(yes_trade_node)
                                individual.memory.append(f'I accepted the trade and it has been executed.')
                                yes_trade_node_ = ConceptNode(len(individual.memorystream.concept_nodes), "trade", system.time, owner.attributes["id"], "trade with", [individual.attributes["id"]], 0, "He accepted the trade and the trade has been executed.", 1)
                                owner.memorystream.add_concept_node(yes_trade_node_)
                                owner.memory.append("He accepted the trade and the trade has been executed.")
                                system.csv_analysis.trade_accepted(owner.attributes["id"])
                                individual.attributes[gainT]-=gainA
                                individual.attributes[payT]+=payA
                                owner.attributes[gainT]+=gainA
                                owner.attributes[payT]-=payA
                              else:
                                if not validO:
                                      owner.memory.append("He accepted the trade but it couldn't go through since I don't have enough resource for it, and I got nothing out of this trade while I lost my action opportunity of today.")
                                      individual.memory.append("I accepted the trade but it couldn't go through because he doesn't have enough resources to pay me accordingly.")
                                      system.csv_analysis.trade_accepted(owner.attributes["id"])
                                if not validI:
                                      owner.memory.append("He accepted the trade but it could't go through because he didn't have enough resources to pay me accordingly. I lost my action opportunity of today.")
                                      individual.memory.append("I accepted the trade but I don't have enough resources to pay him accordingly so it failed to execute.")
                                      system.csv_analysis.trade_accepted(owner.attributes["id"])
                                  
                  #query_judge(f'In response to Person {response_action.owner} initiating {response_action}, {individual.attributes["name"]} chooses to {action}. {add_context}',response_action,individual,system)
            elif not passive:
              ai_action:AIAction = None
              for o in range(5):
                print(action)
                if system.is_stop:
                  print("Stop Simulation!")
                  return
                
                try:
                  action = deserialize_first_json_object(action.lower())
                  ai_action = str_to_ai_action(action, index)
                  break
                except Exception as e:
                  try:
                    ai_action = str_to_ai_action([action[x] for x in action][0], index)
                    action=list(action[x] for x in action)[0]
                    break
                  except Exception as e2:
                    print(f"First Exception:{e}, second exception:{e2}")
                    action:str=query_individual(individual,system,response_action)
                    continue
                
              #Prevent subject to trade with master
              while ai_action.type == AIActionType.Trade and individual.obey_stats.obey_personId == ai_action.targetid:
                action:str=query_individual(individual,system,response_action)
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
              
              #Prevent subject to rob master
              while ai_action.type == AIActionType.Rob and individual.obey_stats.obey_personId == ai_action.targetid:
                action:str=query_individual(individual,system,response_action)
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
              
              #Prevent master to trade with subjects
              while ai_action.type == AIActionType.Trade and ai_action.targetid in individual.obey_stats.subjectid:
                action:str=query_individual(individual,system,response_action)
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
                    farm_node = ConceptNode(len(individual.memorystream.concept_nodes), "farm", system.time, individual.attributes["id"], "farm", [], 0,f'On day {system.time}. I farmed and gained {gain} units of food.', 1)
                    individual.memorystream.add_concept_node(farm_node)
                    individual.memory.append(f'On day {system.time}. I farmed and gained {gain} units of food.')
                    print("Farm is successful.")
              elif ai_action.type==AIActionType.Rob:
                    
                    target=system.individuals[ai_action.targetid]
                    target_master=target.obey_stats.obey_personId
                    if target_master==individual.attributes['id']:
                          pass
                    elif target_master!=-1 and target_master!=individual.obey_stats.obey_personId:
                            rob_target_node = ConceptNode(len(individual.memorystream.concept_nodes), "rob", system.time, individual.attributes["id"], "rob", [target.attributes["id"], target_master], 0, f"I tried to rob {target.attributes['name']}, but it turns out that he is a subject of Person {target_master}, so I am in essense robbing him instead of {target.attributes['name']}.",1)
                            individual.memorystream.add_concept_node(rob_target_node)
                            individual.memory.append(f"I tried to rob {target.attributes['name']}, but it turns out that he is a subject of Person {target_master}, so I am in essense robbing him instead of {target.attributes['name']}.")
                            ai_action.targetid=target_master
                            print(f"Rob target {target.attributes['name']} DEFLECTED to the target's master, Person {target_master}.")
                    append_to_pending_action(ai_action, system)
                  
              elif ai_action.type==AIActionType.Trade:
                    append_to_pending_action(ai_action, system)
              
              elif ai_action.type==AIActionType.Donate:
                target=system.individuals[ai_action.targetid]
                owner = system.individuals[ai_action.ownerid]
                donate(target,owner, system, ai_action.donateType)
                  
              else:
                    print(f'Problem, the type of the action is:{ai_action.type}')
              try:system.history.append(f'{individual.attributes["name"]}:{action["reason"]}')
              except:
                try:system.history.append(f'{individual.attributes["name"]}:{action[[x for x in action][0]]["reason"]}')
                except:system.history.append(f'{individual.attributes["name"]}:\n{action}')
                
              match individual.current_action_type:
                case AIActionType.Farm:
                  system.console_log.append(f"{index}:🌾")
                  system.csv_analysis.farm(index)
                  increase_food(individual)
                case AIActionType.Trade:
                  system.csv_analysis.trade(index)
                  system.console_log.append(f"{index}:🤝")
                case AIActionType.Rob:
                  system.csv_analysis.rob(index)
                  system.console_log.append(f"{index}:🗡️")
                case AIActionType.BeRobbed:
                  system.console_log.append(f"{index}:🛡️")
                case AIActionType.Donate:
                  system.csv_analysis.donate(index)
                  system.console_log.append(f"{index}:D")
                case _ :
                  system.console_log.append(f"{index}:Error")
              individual.attributes['action']=0
              
                     
              
      system.ranking.update({x: x.attributes["social_position"] for x in system.individuals})
      #print(f'OVERALL TRUST LEVEL:{sum([x.attributes["trust_of_others"] for x in system.individuals])}\n\n\n')
      #reach this mean all pending action is done
      pending=False
      sum_action=0
      for i in individuals:
            pending=pending or not i.pending_action.empty()
            sum_action+=i.attributes['action']
      if not pending and not sum_action:
        break
      else:
            print(f'System still pending actions, so will go into another round.')
    day_end(system,individuals)
    system.csv_analysis.log_stat(system, csv_file_name)

    if (system.time % days_between_conversation == 0):
      topic = "Is there anything you think that needs to be changed? What will make your life better?"

      print("Conversation starting...")
      discuss_topic(system, individuals, topic, system.time)
      print("conversation ended")
    # save_logframes(system)
    
# %%
