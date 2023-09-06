import random

import numpy as np
from Main.Individual import Individual
from Main.System import System
#Utils
#Food
FOOD_INCREASE_MIN = 0.9
FOOD_INCREASE_MAX = 1.1
def increase_food(individual:Individual):
    #increase food by random amount between FOOD_INCREASE_MIN and FOOD_INCREASE_MAX
    individual.attributes['food']+=np.random.uniform(FOOD_INCREASE_MIN, FOOD_INCREASE_MAX)*individual.attributes["land"]/3

#Rob
#returns true if individual's strength > enemy's
def compare_strength(individual:Individual, enemy:Individual):
    return individual.attributes["strength"] > enemy.attributes["strength"]

def phi(z):
      return 1.0/(1.0+np.exp(-z))
def winner_loser(person1:Individual,person2:Individual):
      winning_chance1=phi(person1.attributes['strength']-person2.attributes['strength'])
      win1=random.random()>winning_chance1
      return (person1,person2) if win1 else (person2,person1)
  
def rob(target: Individual, rob_person:Individual, system: System, robType: str)->None:
    rob_perosn_id:int=rob_person.attributes['id']
    print(f'To the victim, the win rate is: {target.get_win_rate(rob_perosn_id) if target.robbing_stats.rob_times[rob_perosn_id] else "No rob has been done yet."}')
    winner,loser=winner_loser(target, rob_person,)
    add_context=f'Winner is {winner.attributes["name"]}, loser is {loser.attributes["name"]}.'
    print(f'Additional context:{add_context}')
    winner.add_rob(loser.attributes['id'],True)
    loser.add_rob(winner.attributes['id'],False)
    print(f'Total rob times of the winner: {winner.robbing_stats.total_rob_times}')
    print("Rob times are being added.")
    if winner==target:
            target.attributes['social_position']+=1
            rob_person.attributes['social_position']+=-1
            target.memory.append(f"Day {system.time}. {loser.attributes['name']} tried to rob me, but I rebelled and won. I protected my own land and food and my social position elevated 1 unit.")
            rob_person.memory.append(f"Day {system.time}. I tried to rob {rob_person.attributes['name']}, who rebelled against me and I lost. I did not gain anything and my social position dropped 1 unit.")
    else:
            #Rob Person Successfully Rob Target
            lost_food=target.attributes['food']
            if robType=='food':
                target.attributes['food']-=lost_food
                loser.attributes['food']+=lost_food
                victim_memory=f"I got robbed {lost_food} units of food."
                victor_memory=f"I robbed and gained {lost_food} units of food."
            elif robType=="land":
                if target.attributes['land']>1:
                        target.attributes['land']-=1
                        rob_person.attributes['land']+=1
                        victim_memory=f"I got robbed of 1 land."
                        victor_memory=f"I robbed and gained 1 land."
                else:
                        victim_memory="I have no land to loose."
                        victor_memory="I robbed but he had no land to loose."
            target.attributes['social_position']-=1
            rob_person.attributes['social_position']+=2
            target.memory.append(f"Day {system.time}. {rob_person.attributes['name']} tried to rob me, I rebelled but lost. {victim_memory}. I lost 1 unit of social status.")
            rob_person.memory.append(f"Day {system.time}. I tried to rob {target.attributes['name']}, who rebelled against me but I won. {victor_memory}. I gained 2 units of social status.")