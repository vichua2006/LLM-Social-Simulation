from Main import System
import csv
import numpy as np

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
    self.food_daily = []  
    self.land_daily = []  
    special = [population]
    head = [f"day"]
    for i in range(population):
      head = head + [f"rob_count_{i}", f"rob_rebelled_{i}", f"trade_count_{i}",
                    f"trade_accepted_{i}", f"{i}_obey_to", f"farm_count_{i}", f"produce_luxury_count_{i}", f"consume_luxury_count_{i}", f"food_{i}", f"land_{i}"]
    head.extend(["GDP", "Mean Food", "Median Food", "SD Food", "Richest Food", 
                     "Poorest Food", "Gini Food", "Mean Land", "Median Land", 
                     "SD Land", "Richest Land", "Poorest Land", "Gini Land"]) 
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
      
    self.day_ += 1
    daily_food = []
    daily_land = []
    log = [self.day_]
    total_food_units = 0

    for i in range(self.population):
      individual = system.individuals[i]
      food = individual.attributes['food']
      land = individual.attributes['land']
      daily_food.append(food)
      daily_land.append(land)
      total_food_units += food
      log.extend([self.rob_[i], self.rob_rebel[i], self.trade_[i], self.trade_accept[i],
                        self.obey_[i], self.farm_[i], self.produce_luxury_[i], self.consume_luxury_[i], food, land])
    gdp = total_food_units
    log.append(gdp)
    self.food_daily.append(daily_food)
    self.land_daily.append(daily_land)
    if self.day_ % 2 == 0:
      interval_stats = self.calculate_interval_statistics()
      log.extend(interval_stats)  # Append interval stats to the log
    with open(filename, 'a', newline='') as f:
      csv_writer = csv.writer(f)
      csv_writer.writerow(log)

  def calculate_interval_statistics(self):
        # Calculate statistics for the last 2 days
        food_stats = np.array(self.food_daily[-2:])
        land_stats = np.array(self.land_daily[-2:])

        # Compute mean, median, std, and Gini for both food and land
        food_mean, land_mean = np.mean(food_stats, axis=0), np.mean(land_stats, axis=0)
        food_median, land_median = np.median(food_stats, axis=0), np.median(land_stats, axis=0)
        food_std, land_std = np.std(food_stats, axis=0), np.std(land_stats, axis=0)
        gini_food, gini_land = CsvAnalysis.calculate_gini_coefficient(food_stats.flatten()), CsvAnalysis.calculate_gini_coefficient(land_stats.flatten())

        # Identify richest and poorest for food and land
        total_food, total_land = np.sum(food_stats, axis=0), np.sum(land_stats, axis=0)
        richest_food, poorest_food = np.argmax(total_food), np.argmin(total_food)
        richest_land, poorest_land = np.argmax(total_land), np.argmin(total_land)

        return [food_mean, food_median, food_std, richest_food, poorest_food, gini_food, land_mean, land_median, land_std, richest_land, poorest_land, gini_land]
  
  def calculate_gini_coefficient(data):
        diff_sum = np.sum(np.abs(np.subtract.outer(data, data)))
        return diff_sum / (2 * len(data) * np.sum(data))
