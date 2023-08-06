import numpy as np  # numpy for numerical computations
from typing import List, Dict, Tuple       
from Main.AIAction import AIAction, PendingAction

class Individual:
    pass
class System:   
    def __init__(self,individuals:List[Individual],lands):
        # Each system has a set of pending actions, history, individuals, lands, and rankings
        self.pending_action:Dict[Tuple[int, int], PendingAction]={}#(actor,receiver):action
        self.history=[]
        self.individuals=individuals
        self.land=lands
        self.ranking={}
        for i in individuals:
          self.ranking[i]=0
        self.relations=[x for x in individuals]
        self.time=0
        self.is_stop=False

class Individual:
    def __init__(self, id:int, name:str):
        # Define the characteristics of the individual
        self.attributes = {
            "id": id, # The index of the individual in the system
            "name": name,  # The name of the individual
            "aggressiveness": np.random.uniform(-1, 1),  # Randomly assigned aggressiveness level
            "covetousness": np.random.uniform(0.9, 1.6),  # Randomly assigned covetousness level
            "intelligence": np.random.uniform(0.6, 0.95),  # Randomly assigned intelligence level
            "strength": np.random.uniform(0.5, 0.9),  # Randomly assigned strength level
            "social_position": 0,  # Initial social position is 0
            "land": 10,  # Land owned by the individual
            "food": 2,  # Initial food is 2
            "action": 1  # Initial action point is 1
            ,"trust_of_others":0
        }
        self.current_action:AIAction = AIAction.Default
        self.robbing_stats = RobStats()
        self.obey_stats = ObeyStats()
        # Initialize memory of the individual
        self.memory = ['None']*30
        self.DESIRE_FOR_GLORY=10
        self.DESIRE_FOR_PEACE=3
        
    def add_rob(self, person_id: int, win_rob: bool = False) -> None:   
        self.robbing_stats.total_rob_times += 1

        # Update the total  rob times towards the person
        if person_id in self.robbing_stats.rob_times:
            self.robbing_stats.rob_times[person_id] += 1
        else:
            self.robbing_stats.rob_times[person_id] = 1

        # Update the total win rob times towards the person if applicable
        if win_rob:
            self.robbing_stats.win_rob_times[person_id] + 1
    def obey(self, person_id: int, system:System) -> None:
        self.obey_stats.obey_personId = person_id
        #Get the person you obey to and add yourself to the subject list
        system.individuals[person_id].obey_stats.subject.append(system.individuals.index(self)) 
    
    def change_current_action(self, action: str)->None:
        for a in AIAction:
            if a == action:
                self.current_action = a
                return
    def check_is_responser(self, pending_action:Dict[Tuple[int, int], PendingAction])->None:
        for key in pending_action:
            if key[1] == self.attributes["id"]:
                print(f"Individual {self.attributes['name']} is responser")
                print("pendingActionResponse:", pending_action[key])
                if pending_action[key].type == AIAction.Trade:
                    self.current_action = AIAction.BeTraded
                elif pending_action[key].type == AIAction.Rob:
                    self.current_action = AIAction.BeRobbed
                return True
            
          
  
# Defining a class for rob stats
class RobStats:
    def __init__(self):
        self.total_rob_times: int = 0 #total number of times you rob others
        self.rob_times: Dict[int, int] = {} #key is the personId, value is the number of times you rob this person
        self.win_rob_times: Dict[int, int] = {} #value is the number of times you win the rob against this person

# Defining a class for stats around obey
class ObeyStats:
    def __init__(self) -> None:
        self.obey_personId: int = -1 #the personId you are obey to, -1 means no one is obeyed
        self.subject: List[int] = [] #the personId who obey you