import random

import numpy as np
from Main.Individual import Individual
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