from Main import System
from typing import Optional
import csv
import numpy as np
import json
import os


class CsvAnalysis:
  def __init__(self, population:int, file_name: Optional[str] = None) -> None:
   self.population = population
   self.sorted_individual_wealth = {}
   self.day_=0
   self.previous_gdp = 0 
   self.start_interval_gdp = None
   self.rob_=[0] * population
   self.rob_rebel=[0]*population
   self.farm_=[0] * population
   self.produce_luxury_ = [0] * population
   self.consume_luxury_ = [0] * population
   self.previous_individual_wealth = [0] * population
   self.trade_=[0] * population
   self.trade_accept=[0]*population
   self.donate_ = [0] * population
   self.obey_amount = 0
   self.obey_=[-1] * population
   self.food_daily = [] 
   self.land_daily = []
   self.luxury_goods_daily = []  
   self.food_production_daily = []
   self.luxury_production_daily = []
   special = [population]
   head = [f"day"]
   head.extend(["1st Wealthiest", "2nd Wealthiest", "3rd Wealthiest", "4th Wealthiest", "5th Wealthiest", "6th Wealthiest", "7th Wealthiest", "8th Wealthiest", "9th Wealthiest"])
   for i in range(population):
     head = head + [f"rob_count_{i}", f"rob_rebelled_{i}", f"trade_count_{i}",
                   f"trade_accepted_{i}", f"{i}_obey_to", f"farm_count_{i}", f"produce_luxury_count_{i}", f"consume_luxury_count_{i}", f"food_{i}", f"land_{i}", f"luxury_goods_{i}", f"daily_change_in_wealth_{i}"]
   head.extend(["GDP", "Daily GDP Growth Rate", "Mean Food", "Median Food", "SD Food", "Richest Food (ID | Amount)",
                    "Poorest Food (ID | Amount)", "Gini Food", "Mean Land", "Median Land",
                    "SD Land", "Richest Land (ID | AMount)", "Poorest Land (ID | AMount)", "Gini Land", "Mean Luxury Goods", "Median Luxury Goods", "SD Luxury Goods", "Richest Luxury Goods (ID | Amount)", "Poorest Luxury Goods (ID | Amount)", "Gini Luxury Goods", "Overall Land Mean", "Overall Land Median", "Overall Land Std", "Overall Food Mean", "Overall Food Median", "Overall Food Std", "Overall Luxury Goods Mean", "Overall Luxury Goods Median", "Overall Luxury Goods Std", "Average Luxury Good Production", "Average Food Production", "Good Distribution Ratio (Food/Luxury)", "Trade Initiated Ratio", "Trade Accepted Ratio", "Produce Luxury Ratio", "Produce Food Ratio", "Rob Initiated Ratio", 
                      "GDP Growth"])
   if (file_name != None):
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
   daily_change_in_wealth = [0] * self.population
   if self.obey_amount==self.population-1:
     system.day_end_counter = 1
     with open(filename, 'a', newline='') as f:
       csv_writer = csv.writer(f)
       #csv_writer.writerow(["Common Wealth achived on day "+ str(self.day_)])
    
   self.day_ += 1
   daily_food = []
   daily_land = []
   daily_luxury_goods = []
   food_production_daily = []
   luxury_production_daily = []
   self.calculate_and_sort_wealth(system)
   log = [self.day_]
   total_food_units = 0
   total_luxury_units = 0
   total_food_production_units = 0
   total_luxury_production_units = 0
   top_wealthy_indices = list(self.sorted_individual_wealth.keys())[:9]  # Adjust as needed
   for rank, index in enumerate(top_wealthy_indices, start=1):
        wealth = self.sorted_individual_wealth[index]
        log.append(f"ID: {index} | Wealth: {wealth}")
   


   for i in range(self.population):
     individual = system.individuals[i]
     food = individual.attributes['food']
     land = individual.attributes['land']
     food_production = individual.attributes['food_production_today']
     luxury_production = individual.attributes['luxury_production_today']
     luxury_goods = individual.attributes['luxury_goods']
     current_wealth = luxury_goods * 2 + food
     daily_change_in_wealth[i] = current_wealth - self.previous_individual_wealth[i]
     self.previous_individual_wealth[i] = current_wealth
     daily_food.append(food)
     daily_land.append(land)
     daily_luxury_goods.append(luxury_goods)
     food_production_daily.append(food_production)
     luxury_production_daily.append(luxury_production)
     total_food_units += food
     total_luxury_units += luxury_goods
     total_food_production_units += food_production
     total_luxury_production_units += luxury_production
     
     log.extend([self.rob_[i], self.rob_rebel[i], self.trade_[i], self.trade_accept[i],
                       self.obey_[i], self.farm_[i], self.produce_luxury_[i], self.consume_luxury_[i], food, land, luxury_goods, daily_change_in_wealth[i]])
   gdp = total_food_production_units + 2 * total_luxury_production_units
   if self.previous_gdp != 0:  # To avoid division by zero on the first day
        gdp_growth_rate = ((gdp - self.previous_gdp) / self.previous_gdp) * 100  # Growth rate percentage
   else:
        gdp_growth_rate = 0  # No growth on the first day

    # Update log with GDP growth rate
   

    # Prepare for the next day
   self.previous_gdp = gdp  # Update previous GDP for the next day's calculation

   log.append(gdp)
   log.append(gdp_growth_rate)
   self.food_daily.append(daily_food)
   self.land_daily.append(daily_land)
   self.food_production_daily.append(food_production_daily)
   self.luxury_production_daily.append(luxury_production_daily)
   self.luxury_goods_daily.append(daily_luxury_goods)
   if (self.day_ - 1) % 7 == 0:  # Assuming a 2-day interval; adjust as needed
        self.start_interval_gdp = gdp
   if self.day_ % 7 == 0:
     action_ratios = self.calculate_action_ratios()
     gdp_growth_rate = self.calculate_gdp_growth_rate(gdp)

        # Prepare action ratios and GDP growth for CSV logging
     action_ratios_values = [action_ratios['trade_initiated_ratio'], action_ratios['trade_accepted_ratio'],
                                action_ratios['produce_luxury_ratio'], action_ratios['produce_food_ratio'],
                                action_ratios['rob_initiated_ratio']]
     
     interval_stats = self.calculate_interval_statistics()
     log.extend(interval_stats)  # Append interval stats to the log
     log.extend(action_ratios_values)  # Append action ratios
     log.append(gdp_growth_rate)  # Append GDP growth
   with open(filename, 'a', newline='') as f:
     csv_writer = csv.writer(f)
     csv_writer.writerow(log)


  def calculate_interval_statistics(self):
        # Calculate statistics for the last 2 days
        food_stats = np.array(self.food_daily[-7:])
        land_stats = np.array(self.land_daily[-7:])
        luxury_goods_stats = np.array(self.luxury_goods_daily[-7:])
        luxury_production_stats = np.array(self.luxury_production_daily[-7:])
        food_production_stats = np.array(self.food_production_daily[-7:])


        food_mean, land_mean, luxury_good_mean = np.mean(food_stats, axis=0), np.mean(land_stats, axis=0), np.mean(luxury_goods_stats, axis=0)
        food_median, land_median, luxury_good_median = np.median(food_stats, axis=0), np.median(land_stats, axis=0), np.median(luxury_goods_stats, axis=0)
        food_std, land_std, luxury_goods_std = np.std(food_stats, axis=0), np.std(land_stats, axis=0), np.std(luxury_goods_stats, axis=0)
        gini_food, gini_land, gini_luxury_goods = CsvAnalysis.calculate_gini_coefficient(food_stats.flatten()), CsvAnalysis.calculate_gini_coefficient(land_stats.flatten()), CsvAnalysis.calculate_gini_coefficient(luxury_goods_stats.flatten())


        
        overall_land_mean = np.mean(land_stats)
        overall_land_median = np.median(land_stats)
        overall_land_std = np.std(land_stats)

        overall_food_mean = np.mean(food_stats)
        overall_food_median = np.median(food_stats)
        overall_food_std = np.std(food_stats)

        overall_luxury_mean = np.mean(luxury_goods_stats)
        overall_luxury_median = np.median(luxury_goods_stats)
        overall_luxury_std = np.std(luxury_goods_stats)

        total_food, total_land, total_luxury = np.sum(food_stats, axis=0), np.sum(land_stats, axis=0), np.sum(luxury_goods_stats, axis=0)
        richest_food, poorest_food = np.argmax(total_food), np.argmin(total_food)
        richest_land, poorest_land = np.argmax(total_land), np.argmin(total_land)
        richest_luxury, poorest_luxury = np.argmax(total_luxury), np.argmin(total_luxury)

        richest_food_value, poorest_food_value = total_food[richest_food], total_food[poorest_food]
        richest_land_value, poorest_land_value = total_land[richest_land], total_land[poorest_land]
        richest_luxury_value, poorest_luxury_value = total_land[richest_luxury], total_land[poorest_luxury]

      
        richest_food_str = f"{richest_food}|{richest_food_value}"
        poorest_food_str = f"{poorest_food}|{poorest_food_value}"
        richest_land_str = f"{richest_land}|{richest_land_value}"
        poorest_land_str = f"{poorest_land}|{poorest_land_value}"
        richest_luxury_str = f"{richest_luxury}|{richest_luxury_value}"
        poorest_luxury_str = f"{poorest_luxury}|{poorest_luxury_value}"
        
        overall_luxury_production_mean = np.mean(luxury_production_stats)
        overall_food_production_mean = np.mean(food_production_stats)
        total_food_production = np.sum(food_production_stats)
        total_luxury_production = np.sum(luxury_production_stats)  
        if total_luxury_production > 0:
          good_distribution_ratio = total_food_production / total_luxury_production
        else:
          good_distribution_ratio = "undefined"

        return [food_mean, food_median, food_std, richest_food_str, poorest_food_str, gini_food, land_mean, land_median, land_std, richest_land_str, poorest_land_str, gini_land, luxury_good_mean, luxury_good_median, luxury_goods_std, richest_luxury_str, poorest_luxury_str, gini_luxury_goods, overall_land_mean, overall_land_median, overall_land_std, overall_food_mean, overall_food_median, overall_food_std, overall_luxury_mean, overall_luxury_median, overall_luxury_std, overall_luxury_production_mean, overall_food_production_mean, good_distribution_ratio]
  def calculate_gini_coefficient(data):
       diff_sum = np.sum(np.abs(np.subtract.outer(data, data)))
       return diff_sum / (2 * len(data) * np.sum(data))
 
 
  
 
  def calculate_action_ratios(self):
    # Summing up the counts for each action over the 7-day period
    total_trade_initiated = sum(self.trade_)
    total_trade_accepted = sum(self.trade_accept)
    total_produce_luxury = sum(self.produce_luxury_)
    total_produce_food = sum(self.farm_)
    total_rob_initiated = sum(self.rob_)
    # Calculating the total number of targeted actions
    total_actions = total_trade_initiated + total_trade_accepted + total_produce_luxury + total_produce_food + total_rob_initiated
    # Calculating ratios for each targeted action
    ratios = {
        'trade_initiated_ratio': total_trade_initiated / total_actions if total_actions > 0 else 0,
        'trade_accepted_ratio': total_trade_accepted / total_actions if total_actions > 0 else 0,
        'produce_luxury_ratio': total_produce_luxury / total_actions if total_actions > 0 else 0,
        'produce_food_ratio': total_produce_food / total_actions if total_actions > 0 else 0,
        'rob_initiated_ratio': total_rob_initiated / total_actions if total_actions > 0 else 0,
    }
    return ratios
  def calculate_gdp_growth_rate(self, current_gdp):
        # Check if start_interval_gdp is set
        if self.start_interval_gdp is not None:
            # Calculate and return GDP growth rate
            gdp_growth_rate = ((current_gdp - self.start_interval_gdp) / self.start_interval_gdp) * 100
            return gdp_growth_rate
        else:
            # Return "N/A" or another placeholder if start_interval_gdp is not set
            return "N/A"
        
  def calculate_and_sort_wealth(self, system):
    # Initial dictionary for individual wealth
    individual_wealth = {}

    for i in range(self.population):
        individual = system.individuals[i]
        # Calculate wealth based on luxury goods and food values
        wealth = (individual.attributes['luxury_goods'] * 2) + individual.attributes['food']
        individual_wealth[individual.attributes['name']] = wealth  # Use individual's name as key and wealth as value

    # Sort the dictionary by wealth in descending order and return a dictionary
    sorted_individual_wealth = dict(sorted(individual_wealth.items(), key=lambda item: item[1], reverse=True))

    # Store the sorted dictionary for further use or logging
    self.sorted_individual_wealth = sorted_individual_wealth


  def report_to_soverign(self, system: System):
    '''
    computes and returns all data needed for soverign to make decisions
    MUST be called before log_stat is called in a simulation day
    '''

    individuals = system.individuals

    # calculate all data 
    
    food_mean, food_median, food_std, richest_food_str, poorest_food_str, gini_food, \
    land_mean, land_median, land_std, richest_land_str, poorest_land_str, gini_land, \
    luxury_good_mean, luxury_good_median, luxury_goods_std, richest_luxury_str, poorest_luxury_str, gini_luxury_goods, \
    overall_land_mean, overall_land_median, overall_land_std, overall_food_mean, overall_food_median, overall_food_std, \
    overall_luxury_mean, overall_luxury_median, overall_luxury_std, overall_luxury_production_mean, overall_food_production_mean, good_distribution_ratio = self.calculate_interval_statistics()

    # re-sort wealth by person
    self.calculate_and_sort_wealth(system)
    individual_wealth = self.sorted_individual_wealth

    # compute the change in wealth of each person
    person_change_in_wealth = {}
    for i in range(self.population):
      individual = individuals[i]
      food = individual.attributes['food']
      land = individual.attributes['land']
      luxury_goods = individual.attributes['luxury_goods']
      current_wealth = luxury_goods * 2 + food
      person_change_in_wealth[individual.attributes['name']] = current_wealth - self.previous_individual_wealth[i]

    # compute GDP
    total_food_units = sum([i.attributes['food'] for i in individuals])
    total_luxury_units = sum([i.attributes['luxury_goods'] for i in individuals])
    gdp = total_food_units + 2 * total_luxury_units

    # compute dGDP
    if self.previous_gdp != 0:  # To avoid division by zero on the first day
          daily_gdp_growth_rate = ((gdp - self.previous_gdp) / self.previous_gdp) * 100  # Growth rate percentage
    else:
          daily_gdp_growth_rate = 0  # No growth on the first day
    
    # compute the activity ratios and format them into a string
    activity_ratios = self.calculate_action_ratios()
    activity_ratio_str = ", ".join([f"{action}: {rate}" for action, rate in activity_ratios.items()])

    # mean_production value 
    return overall_food_std, overall_food_mean, overall_land_std, overall_land_mean, individual_wealth, gini_food, gini_land, person_change_in_wealth, gdp, daily_gdp_growth_rate, overall_food_production_mean, activity_ratio_str, good_distribution_ratio

  def output_individual_stats(self, system:System, dir_name:str):
      # produce two text files: one lists all information about each person per day, the other lists all information over all days per each person
      individuals = system.individuals
      combined_stats = [json.loads(p.get_log_list()) for p in individuals]

      by_person = []
      by_day = []

      days = system.time

      # generate the by_day list
      for i in range(days):
         day_data = {"day": i, "stats": []}
         for stats in combined_stats:
            day_data["stats"].append(stats[i])
         by_day.append(day_data)
      
      # generate the by_person list
      for i, stats in enumerate(combined_stats):
         by_person.append({"name":individuals[i].attributes["name"], "stats":stats})
      
      by_person_filename = f"{dir_name}/stats_by_person.txt"
      by_day_filename = f"{dir_name}/stats_by_day.txt"

      if not (os.path.exists(dir_name)):
        os.mkdir(dir_name)
      
      with open(by_person_filename, "w") as bpf, open(by_day_filename, "w") as bdf:
        bpf.write(json.dumps(by_person, indent=4))
        bdf.write(json.dumps(by_day, indent=4))
      