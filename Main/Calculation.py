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
  
def share_rob_gain(master: Individual, robAmount: float, robType: str, system:System) -> None:
    if master.obey_stats.subject is None or not master.obey_stats.subject:
        print("SHARE_ROB_FOOD: no subject, directly get the rob amount.")
        master.attributes[robType]+=robAmount
        return
    #divide the rob amount to each subject
    for subjectid in master.obey_stats.subject:
        subject = system.individuals[subjectid]
        subject.attributes[robType]+=robAmount/len(master.obey_stats.subject)
        subjectid.memory.append(f"Day {master.system.time}. I got {robAmount/len(master.obey_stats.subject)} units of {robType} from {master.attributes['name']}.")
    #include the master
    master.attributes[robType]+=robAmount/len(master.obey_stats.subject)
    master.memory.append(f"Day {master.system.time}. I gave {robAmount} units of {robType} to my subjects.")
    print(f"SHARE_ROB_FOOD: {master.attributes['name']} shared {robAmount} units of {robType} to {len(master.obey_stats.subject)} subjects.")
    return
    
def rob(target: Individual, rob_person:Individual, system: System, robType: str)->None:
    rob_perosn_id:int=rob_person.attributes['id']
    print(f'To the victim, the win rate is: {target.get_win_rate(rob_perosn_id) if target.robbing_stats.rob_times[rob_perosn_id] else "No rob has been done yet."}')
    winner,loser=winner_loser(target, rob_person,)
    add_context=f'Winner is {winner.attributes["name"]}, loser is {loser.attributes["name"]}.'
    print(f'Additional context:{add_context}')
    winner.add_rob(loser.attributes['id'],True)
    loser.add_rob(winner.attributes['id'],False)
    print(f'Total rob times of the winner: {winner.robbing_stats.total_rob_times}')
    
    if winner==target:
            target.attributes['social_position']+=1
            rob_person.attributes['social_position']+=-1
            target.memory.append(f"Day {system.time}. {rob_person.attributes['name']} tried to rob me, but I rebelled and won. I protected my own land and food and my social position elevated 1 unit.")
            rob_person.memory.append(f"Day {system.time}. I tried to rob {rob_person.attributes['name']}, who rebelled against me and I lost. I did not gain anything and my social position dropped 1 unit.")
    else:
            victim_memory = ""
            #Rob Person Successfully Rob Target
            lost_food:float=target.attributes['food']
            if robType=='food':
                target.attributes['food']-=lost_food
                share_rob_gain(rob_person,lost_food,robType, system)
                victim_memory=f"I got robbed {lost_food} units of food."
                victor_memory=f"I robbed and gained {lost_food} units of food."
            elif robType=="land":
                if target.attributes['land']>1:
                        target.attributes['land']-=1
                        share_rob_gain(rob_person,lost_food,robType, system)
                        victim_memory=f"I got robbed of 1 land."
                        victor_memory=f"I robbed and gained 1 land."
                else:
                        victim_memory="I have no land to loose."
                        victor_memory="I robbed but he had no land to loose."
            target.attributes['social_position']-=1
            rob_person.attributes['social_position']+=2
            target.memory.append(f"Day {system.time}. {rob_person.attributes['name']} tried to rob me, I rebelled but lost. {victim_memory}. I lost 1 unit of social status.")
            rob_person.memory.append(f"Day {system.time}. I tried to rob {target.attributes['name']}, who rebelled against me but I won. {victor_memory}. I gained 2 units of social status.")
    return

#master punish subject, get his food and land and share it to other subjects except the subject being punished
def punishment(subject:Individual, system:System) -> None:
    if subject.obey_stats.obey_personId==-1:
        print("PUNISHMENTERROR: no master, this should not happen.")
        return
    print(f"PUNISHMENT: {subject.attributes['name']} is punished by {system.individuals[subject.obey_stats.obey_personId].attributes['name']}, all other subjects will share the food and land of {subject.attributes['name']}.")
    subject.memory.append(f"I was punished by {system.individuals[subject.obey_stats.obey_personId].attributes['name']} because I, as a subject, rob other subject.")
    master.memory.append(f"I punished {subject.attributes['name']} because he, as a subject, rob other subject.")
    master = system.individuals[subject.obey_stats.obey_personId]
    #master punish subject, 50% food and 50% land
    food_amount = 0.5 * subject.attributes['food']
    land_amount = 0.5 * subject.attributes['land']
    subject.attributes['food'] -= food_amount
    subject.attributes['land'] -= land_amount
    #share the food and land to other subjects
    for subjectid in master.obey_stats.subject:
        if subjectid!=subject.attributes['id']:
            subject.memory.append(f"I got food and land because {subject.attributes['name']} was punished by {master.attributes['name']}, since he robbed other subject.")
            subject = master.system.individuals[subjectid]
            subject.attributes['food'] += food_amount/(len(master.obey_stats.subject)-1)
            subject.attributes['land'] += land_amount/(len(master.obey_stats.subject)-1)
    return