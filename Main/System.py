from typing import List
from GUI.CustomConsoleLog import CustomConsoleLog     
from PySimpleGUI.PySimpleGUI import Window
import Main.Bank as Bank

from Main.CsvAnalysis import CsvAnalysis 
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
        self.day_end_counter=0
        self.should_stop=False
        self.food_factor = [1] * len(individuals)
        self.trade_factor = [1] * len(individuals)
        self.lux_factor = [1] * len(individuals)
        self.bank = Bank.Bank()
        self.individual_count = len(individuals)
        self.max_indivisual_index = len(individuals)
        self.deaths = 0

    def production_factor(self, ratio, index):
        self.food_factor[index] *= ratio

    def trade_factor(self, ratio, index):
        self.trade_factor[index] *= ratio
    
    def luxuray_factor(self, ratio, index):
        self.lux_factor[index] *= ratio
        
    def set_csv_analysis(self, csv_analysis:CsvAnalysis):
        self.csv_analysis = csv_analysis
        
    def set_console_log(self, console_log:CustomConsoleLog):
        self.console_log = console_log
    def set_window(self, window:Window):
        self.window = window
        
    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, state):
        self.__dict__.update(state)