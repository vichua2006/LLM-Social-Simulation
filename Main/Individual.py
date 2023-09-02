import numpy as np  # numpy for numerical computations
from typing import List, Dict, Tuple
from Main.AIAction import AIActionType, AIAction, RobAction
import queue
from Main.System import System

class SeralizeQueue(queue.Queue):
    def __getstate__(self):
        return list(self.queue)
    def __setstate__(self, state):
        self.__init__()
        self.queue = state
        
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
        self.pending_action:SeralizeQueue[AIAction] = SeralizeQueue() # The pending action that the individual need to deal with
        self.current_action_type:AIActionType = AIActionType.Default
        self.robbing_stats = RobStats()
        self.obey_stats = ObeyStats()
        # Initialize memory of the individual
        self.memory = ['None']*30
        self.DESIRE_FOR_GLORY=10
        self.DESIRE_FOR_PEACE=3

    def get_pending_action_as_list(self):
        return list(self.pending_action.queue)
    
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
        #if already obey to anyone, directly return
        if self.obey_stats.obey_personId!=-1:
            print("LOGICAL ERROR:ALREADY OBEY TO SOMEONE")
            return
        if person_id==self.attributes['id']:
            print("LOGICAL ERROR:CANNOT OBEY TO SELF")
            return
        #obey to the obyer's obeyer if applicable
        master=system.individuals[person_id].obey_stats.obey_personId
        while master!=-1:
            person_id=master
            master=system.individuals[person_id].obey_stats.obey_personId
        self.obey_stats.obey_personId = person_id
        #Get the person you obey to and add yourself to the subject list
        system.individuals[person_id].obey_stats.subject.append(system.individuals.index(self)) 
        #iterate all subject of yours and transfer its obeyperson to the person you obey to
        subjects=[x for x in self.obey_stats.subject]
        for subject in subjects:
            system.individuals[subject].obey_stats.obey_personId = person_id
            system.individuals[person_id].obey_stats.subject.append(subject)
        self.obey_stats.subject=[]
        
        
    
    # Check if the individual is the responser of the action
    def check_is_responser(self, action:AIAction)->None:
        match action.type:
            case AIActionType.Rob:
                self.current_action_type = AIActionType.BeRobbed
            case AIActionType.Trade:
                self.current_action_type = AIActionType.BeTraded
    
    
          
  
# Defining a class for rob stats
class RobStats():
    def __init__(self):
        self.total_rob_times: int = 0 #total number of times you rob others
        self.rob_times: Dict[int, int] = {} #key is the personId, value is the number of times you rob this person
        PEOPLE=30
        self.win_rob_times: Dict[int, int] = {} #value is the number of times you win the rob against this person
        for i in range(PEOPLE):
            self.rob_times[i]=0
            self.win_rob_times[i]=0
    #JSON serialization
    def __json_encode__(self):
        return self.__dict__

    #JSON deserialization
    @classmethod
    def __json_decode__(cls, dct):
        obj = cls()
        obj.__dict__.update(dct)
        return obj

    
# Defining a class for stats around obey
class ObeyStats:
    def __init__(self) -> None:
        self.obey_personId: int = -1 #the personId you are obey to, -1 means no one is obeyed
        self.subject: List[int] = [] #the personId who obey you
    def to_dict(self) -> Dict:
        return {
            'obey_personId': self.obey_personId,
            'subject': self.subject
        }

    @classmethod
    def from_dict(cls, data: Dict):
        obj = cls()
        obj.obey_personId = data['obey_personId']
        obj.subject = data['subject']
        return obj