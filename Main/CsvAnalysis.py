from Main import System
import csv

class CsvAnalysis:
  def __init__(self, population:int, file_name:str) -> None:
    self.population = population
    self.day_=0
    self.rob_=[0] * population
    self.rob_rebel=[0]*population
    self.farm_=[0] * population
    self.produce_luxury_ = [0] * population
    self.consume_luxury_ = [0] * population
    self.trade_=[0] * population
    self.trade_accept=[0]*population
    self.donate_ = [0] * population
    self.obey_amount = 0
    self.obey_=[-1] * population
    special = [population]
    head = [f"day"]
    for i in range(population):
      head = head + [f"rob_count_{i}", f"rob_rebelled_{i}", f"trade_count_{i}",
                    f"trade_accepted_{i}", f"{i}_obey_to", f"farm_count_{i}", f"produce_luxury_count_{i}", f"consume_luxury_count_{i}"]
    with open(file_name, 'a', newline='') as f:
      csv_writer = csv.writer(f)
      csv_writer.writerow(head)
  
  def trade(self, index):
    self.trade_[index]+=1
  
  def farm(self, index):
    self.farm_[index]+=1
  
  def produce_luxury(self, index):
    self.produce_luxury_[index] += 1

  def consume_luxury(self, index):
    self.consume_luxury_[index] += 1
    
  def rob(self, index):
    self.rob_[index]+=1
  
  def donate(self, index):
    self.donate_[index]+=1
    
  def trade_accepted(self, index):
    self.trade_accept[index]+=1
    
  def rob_rebelled(self, index):
    self.rob_rebel[index]+=1
    
  # index obey to target
  def obey(self, system):
    for person in system.individuals:
      self.obey_[person.attributes["id"]]=person.obey_stats.obey_personId
    count = 0
    for b in self.obey_:
      if b != -1:
        count +=1
    self.obey_amount=count
    
  def log_stat(self, system, filename:str):
    if self.obey_amount==self.population-1:
      system.day_end_counter = 1 
      with open(filename, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        #csv_writer.writerow(["Common Wealth achived on day "+ str(self.day_)])
      
    self.day_+=1
    log = [self.day_]
    for i in range(self.population):
      log =  log + [self.rob_[i], self.rob_rebel[i], self.trade_[i], self.trade_accept[i],
            self.obey_[i], self.farm_[i], self.produce_luxury_[i], self.consume_luxury_[i]]
    with open(filename, 'a', newline='') as f:
      csv_writer = csv.writer(f)
      csv_writer.writerow(log)
