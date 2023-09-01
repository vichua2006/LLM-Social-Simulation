from typing import List
from GUI.CustomConsoleLog import CustomConsoleLog      
class Individual:
    pass

class System:   
    def __init__(self,individuals:List[Individual],lands):
        # Each system has a set of pending actions, history, individuals, lands, and rankings
        self.history=[]
        self.individuals:List[Individual] =individuals
        self.land=lands
        self.ranking={}
        for i in individuals:
          self.ranking[i]=0
        self.relations=[x for x in individuals]
        self.time=0
        self.is_stop=False
        self.obey_frequence=[]
        
    def set_console_log(self, console_log:CustomConsoleLog):
        self.console_log = console_log

