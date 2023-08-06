import random
from Main.Individual import Individual
#Utils
#Food
FOOD_INCREASE_MIN = 0.1
FOOD_INCREASE_MAX = 0.5
def increase_food(individual:Individual):
    #increase food by random amount between FOOD_INCREASE_MIN and FOOD_INCREASE_MAX
    individual.attributes["food"] += random.uniform(FOOD_INCREASE_MIN, FOOD_INCREASE_MAX)

#Rob
#returns true if individual's strength > enemy's
def compare_strength(individual:Individual, enemy:Individual):
    return individual.attributes["strength"] > enemy.attributes["strength"]
