import jsonpickle
import threading
from typing import List
from Main.Calculation import increase_food, punishment, rob, winner_loser
from Main.Individual import Individual
from Main.System import System
from Main.Query import query_individual
from Main.StringUtils import deserialize_first_json_object
from Main.AIAction import AIAction, AIActionType
from Main.PendingAction import append_to_pending_action, str_to_ai_action
from Main.SaveLoad import init_save, save_logframes
import random
import datetime
import csv

population=9
file_name='Log/'+datetime.datetime.now().strftime("%B %d, %I %M%p , %Y")+'Experimentlog.csv'
class analysis:
  def __init__(self, population:int) -> None:
    self.day_=1
    self.rob_=[0] * population
    self.rob_accept=[0]*population
    self.farm_=[0] * population
    self.trade_=[0] * population
    self.trade_accept=[0]*population
    self.obey_amount = 0
    self.obey_=[-1] * population
    head = []
    for i in range(population):
      head = head + [f"rob_count_{i}", f"rob_accepted_{i}", f"trade_count_{i}",
                    f"trade_accepted_{i}", f"obey_to_{i}", f"farm_count_{i}"]
    with open(file_name, 'a', newline='') as f:
      csv_writer = csv.writer(f)
      csv_writer.writerow(head)
  
  def trade(self, index):
    self.trade_[index]+=1
  
  def farm(self, index):
    self.farm_[index]+=1
    
  def rob(self, index):
    self.rob_[index]+=1
    
  def trade_accepted(self, index):
    self.trade_accept[index]+=1
    
  def rob_accepted(self, index):
    self.rob_accept[index]+=1
    
  def obey(self, index, target):
    self.obey_[index]=target
    count = 0
    for b in self.obey_:
      if b != -1:
        count +=1
    self.obey_amount=count
    
  def log_stat(self):
    if self.obey_amount==population-1:
      with open(file_name, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Common Wealth achived on day "+ str(self.day_)])
      
    self.day_+=1
    log = []
    for i in range(population):
      log =  log + [self.rob_[i], self.rob_accepted[i], self.trade_[i], self.trade_accepted[i],
            self.obey_[i], self.farm_[i]]
    with open(file_name, 'a', newline='') as f:
      csv_writer = csv.writer(f)
      csv_writer.writerow(log)

stat = analysis(population)

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
    POPULATION=population
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
    # init_save(system)
    return system

def simulate(individuals:List[Individual],system:System):
    while True:
      for individual in individuals:
          if system.is_stop:
            print("Stop Simulation!")
            return
          index:int = individuals.index(individual)
          passive=not individual.pending_action.empty()
          while individual.attributes['action']>0 or passive:
            passive=not individual.pending_action.empty()
            print(f"Person {index} is responding...\n")
            response_action: AIAction = individual.pending_action.get() if passive else None
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
                        stat.update_obey(system)
                        print("DETECT: subject rob subject, pushiment will be given.")
                        punishment(owner, system)
                      
                      elif R:
                        rob(individual, owner, system, response_action.robType)
                      elif not R:
                            #if master rob subject, subject will accept instead of obey, where obey only refer to the first obey that happen between two individuals without subject-master relationship
                            if owner.attributes["id"] !=  individual.obey_stats.obey_personId:
                              owner.add_rob(individual.attributes['id'],True)
                              stat.obey(owner.attributes["id"], individual.attributes["id"])
                              system.console_log.append(f"{individual.attributes['id']}: Obey {response_action.ownerid}")
                              individual.obey(response_action.ownerid,system)
                              owner.memory.append(f"I tried to robbed {individual.attributes['name']}, he obeyed me and has became my subject, to whom I can do anything without worrying about being betrayed.")
                              individual.memory.append(f"I obeyed to {owner.attributes['name']} and now I have to listen to all his commands and can never betray him.")
                            else:
                              owner =system.individuals[response_action.ownerid]
                              owner.add_rob(individual.attributes['id'],True)
                              system.console_log.append(f"{individual.attributes['id']}: Accept robbery from {response_action.ownerid}")
                              print("success accepting robbery from master")
                              stat.rob_accepted(owner.attributes["id"])
                  elif response_action.type==AIActionType.Trade:
                        owner.memory.append(f"Day {system.time}. I initiated a trade to {individual.attributes['name']}, which is to exchange {response_action.payAmount} units of my {response_action.payType} for {response_action.gainAmount} units of his {response_action.gainType}.")
                        individual.memory.append(f"Day {system.time}.{response_action.ownerid} initiated a trade offer to me, which is to exchange his {response_action.payAmount} units of {response_action.payType} for {response_action.gainAmount} units of my {response_action.gainType}. ")
                        if R:
                              individual.memory.append(f'I rejected the trade offer by {response_action.ownerid}.')
                              owner.memory.append(f"But he rejected it so I gained nothing and exhausted my action opportunity of today.")
                        elif not R:
                              gainT=response_action.gainType
                              gainA=response_action.gainAmount
                              payA=response_action.payAmount
                              payT=response_action.payType
                              validO=owner.attributes[payT]>=payA
                              validI=individual.attributes[gainT]>=gainA#ADD conditionals here to invalidate unrealisitic trade offers
                              if validO and validI:
                                individual.memory.append(f'I accepted the trade and it has been executed.')
                                owner.memory.append("He accepted the trade and the trade has been executed.")
                                stat.trade_accepted(owner.attributes["id"])
                                individual.attributes[gainT]-=gainA
                                individual.attributes[payT]+=payA
                                owner.attributes[gainT]+=gainA
                                owner.attributes[payT]-=payA
                              else:
                                if not validO:
                                      owner.memory.append("He accepted the trade but it couldn't go through since I don't have enough resource for it, and I got nothing out of this trade while I lost my action opportunity of today.")
                                      individual.memory.append("I accepted the trade but it couldn't go through because he doesn't have enough resources to pay me accordingly.")
                                      stat.trade_accepted(owner.attributes["id"])
                                if not validI:
                                      owner.memory.append("He accepted the trade but it could't go through because he didn't have enough resources to pay me accordingly. I lost my action opportunity of today.")
                                      individual.memory.append("I accepted the trade but I don't have enough resources to pay him accordingly so it failed to execute.")
                                      stat.trade_accepted(owner.attributes["id"])
                                  
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
              is_subject = "False"
              for id in individual.obey_stats.subjectid:
                if id == ai_action.targetid:
                  is_subject = "True"
              
              while ai_action.type == AIActionType.Trade and is_subject == "True":
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
                    individual.memory.append(f'On day {system.time}. I farmed and gained {gain} units of food.')
                    print("Farm is successful.")
              elif ai_action.type==AIActionType.Rob:
                    
                    target=system.individuals[ai_action.targetid]
                    target_master=target.obey_stats.obey_personId
                    if target_master==individual.attributes['id']:
                          pass
                    elif target_master!=-1:
                            individual.memory.append(f"I tried to rob {target.attributes['name']}, but it turns out that he is a subject of Person {target_master}, so I am in essense robbing him instead of {target.attributes['name']}.")
                            ai_action.targetid=target_master
                            print(f"Rob target {target.attributes['name']} DEFLECTED to the target's master, Person {target_master}.")
                    append_to_pending_action(ai_action, system)
                  
              elif ai_action.type==AIActionType.Trade:
                    append_to_pending_action(ai_action, system)
                  
              else:
                    print(f'Problem, the type of the action is:{ai_action.type}')
              try:system.history.append(f'{individual.attributes["name"]}:{action["reason"]}')
              except:
                try:system.history.append(f'{individual.attributes["name"]}:{action[[x for x in action][0]]["reason"]}')
                except:system.history.append(f'{individual.attributes["name"]}:\n{action}')
                
              match individual.current_action_type:
                case AIActionType.Farm:
                  system.console_log.append(f"{index}:🌾")
                  stat.farm(index)
                  increase_food(individual)
                case AIActionType.Trade:
                  stat.trade(index)
                  system.console_log.append(f"{index}:🤝")
                case AIActionType.Rob:
                  stat.rob(index)
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
    stat.log_stat()
    # save_logframes(system)

# %%
