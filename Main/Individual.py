from __future__ import annotations # Allow self-reference in type annotations
import numpy as np  # numpy for numerical computations
from typing import Any, List, Dict, Tuple, Optional, Callable, Literal, Union
from Main.AIAction import AIActionType, AIAction, RobAction
import queue
from Main.System import System
from Main.Memory import MemoryStream
from Main.SpeakingAgent import SpeakingAgent
from Main.config import AUTOGEN_LLM_CONFIG
from Main.Personalities import generate_personality



class SeralizeQueue(queue.Queue):
    def __getstate__(self):
        return list(self.queue)
    
    def __setstate__(self, state:List[AIAction]):
        self.__init__()
        #List to queue
        for action in state:
            self.put(action)
        
class Individual:
    def __init__(self, id:int, name:str):
        # Define the characteristics of the individual
        long_tail_sampler=np.random.gamma(2.0,0.9) #sampling from long tail
        land=int(10*long_tail_sampler+1) #+1 so that no one has zero land
        food=int(land**1.3) # land compounds so as exponetial effect to food.

        self.attributes = {
            "id": id, # The index of the individual in the system
            "name": name,  # The name of the individual
            "strength": np.random.normal(0.7, 0.2),  # Randomly assigned strength level
            "social_position": 0,  # Initial social position is 0
            "luxury_goods": 0, # Initial luxury goods is 0
            "action": 1,  # Initial action point is 1
            "trust_of_others":0,
            "starved":0,
            "land": land,  # Land owned by the individual
            "food": food,  # Initial food as long tail distribution
            "action": 1  # Initial action point is 1
            ,"trust_of_others":0
        }
        
        # Individual specific production numbers
        self.food_production = 0
        self.luxury_production = 0
        
        self.INTELLIGENCE=1#np.random.beta(100,10)
        self.pending_action:SeralizeQueue[AIAction] = SeralizeQueue() # The pending action that the individual need to deal with
        self.current_action_type:AIActionType = AIActionType.Default
        self.robbing_stats = RobStats()
        self.obey_stats = ObeyStats()
        self.memorystream = MemoryStream(id)
        # Initialize memory of the individual
        self.memory = ['None']*30
        self.DESIRE_FOR_GLORY=10
        self.DESIRE_FOR_PEACE=3
        # Initialize autogen agent of the individual
        # system message is updated by the converse() function
        self.agent = SpeakingAgent(
            name=self.attributes["name"],
            system_message=self.attributes["name"],
            llm_config=AUTOGEN_LLM_CONFIG
        )

        # a list of 5 strings, denoting the person's openness, conscientiousness, agreeableness, neuroticism respectively
        self.personalities = generate_personality()

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
    
        #return the person id if all individual obey to the same person except for the person who is obeyed
    def check_is_common_wealth(self, system:System)->bool:
        obey_person_id:int = self.obey_stats.obey_personId
        if obey_person_id==-1:
            return -1
        for individual in system.individuals:
            if individual.obey_stats.obey_personId!=obey_person_id and individual.attributes['id']!=obey_person_id:
                return -1
        return obey_person_id
        
        
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
        system.individuals[person_id].obey_stats.subjectid.append(system.individuals.index(self)) 
        #iterate all subject of yours and transfer its obeyperson to the person you obey to
        subjects=[x for x in self.obey_stats.subjectid]
        for subject in subjects:
            system.individuals[subject].obey_stats.obey_personId = person_id
            system.individuals[person_id].obey_stats.subjectid.append(subject)
        self.obey_stats.subjectid=[]
        
        common_wealth_id = self.check_is_common_wealth(system)
        if common_wealth_id!=-1:
            system.window.write_event_value('-COMMONWEALTH-', common_wealth_id)
            

    
    # Check if the individual is the responser of the action
    def check_is_responser(self, action:AIAction)->None:
        match action.type:
            case AIActionType.Rob:
                self.current_action_type = AIActionType.BeRobbed
            case AIActionType.Trade:
                self.current_action_type = AIActionType.BeTraded
    
    def get_win_rate(self, target:Individual):
        return self.robbing_stats.win_rob_times[target]/self.robbing_stats.rob_times[target]
    
    def get_agent(self):
        # return the agent variable
        return self.agent
    
    def get_personality(self) -> List[str]:
        return self.personalities
    
    def update_agent_prompt(self, prompt:str):
        # updates the agent's system message and description
        self.agent.update_system_message(prompt)
    
    def update_agent_speaking_tendency(self, prompt:str):
        self.agent.update_speaking_tendency(prompt)

    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, state):
        self.__dict__.update(state)
  
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
    def get_rob_times_list(self):
        return [f"{key}:{value}" for key, value in self.rob_times.items()]
    
    def __getstate__(self):
        return self.__dict__
    #JsonPickle will transfer the Dict[int, int] to Dict[str, int], so we need to transfer it back
    def __setstate__(self, state):
        self.__init__()
        #if get the value, then get, else use the default value
        self.total_rob_times=state.get("total_rob_times", self.total_rob_times)
        self.rob_times=state.get("rob_times", self.rob_times)
        self.win_rob_times=state.get("win_rob_times", self.win_rob_times)        
        #str to int
        self.rob_times={int(key):value for key, value in self.rob_times.items()}
        self.win_rob_times={int(key):value for key, value in self.win_rob_times.items()}
    
# Defining a class for stats around obey
class ObeyStats:
    def __init__(self) -> None:
        self.obey_personId: int = -1 #the personId you are obey to, -1 means no one is obeyed
        self.subjectid: List[int] = [] #the personId who obey you
