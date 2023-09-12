from typing import List
from GUI.CustomConsoleLog import CustomConsoleLog     
from PySimpleGUI.PySimpleGUI import Window 
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
        #self.relations=[x for x in individuals]
        self.time=0
        self.is_stop=False
        self.obey_frequence=[]
        
    def set_console_log(self, console_log:CustomConsoleLog):
        self.console_log = console_log
    def set_window(self, window:Window):
        self.window = window
        
    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, state):
        self.__dict__.update(state)