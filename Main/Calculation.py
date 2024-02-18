import random

import numpy as np
from Main.Individual import Individual
from Main.System import System
#Utils
#Food
def increase_food(individual:Individual):
    # Increase food based on individual's production #
    gain = round(individual.food_production * individual.attributes["land"] / 3)
    individual.attributes['food'] += gain
    return gain
    
# Luxury Good
def increase_luxury(individual: Individual):
    # Increase luxury goods based on individual's production #
    gain = round(individual.luxury_production * individual.attributes["land"] / 3)
    individual.attributes["luxury_goods"] += gain
    return gain

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
    if master.obey_stats.subjectid is None or not master.obey_stats.subjectid:
        print("SHARE_ROB_FOOD: no subject, directly get the rob amount.")
        master.attributes[robType]+=robAmount
        return
    #divide the rob amount to each subject
    for subjectid in master.obey_stats.subjectid:
        subject = system.individuals[subjectid]
        subject.attributes[robType]+=robAmount/len(master.obey_stats.subjectid)
        subject.memory.append(f"Day {system.time}. I got {robAmount/len(master.obey_stats.subjectid)} units of {robType} from {master.attributes['name']}.")
    #include the master
    master.attributes[robType]+=robAmount/len(master.obey_stats.subjectid)
    master.memory.append(f"Day {system.time}. I gave {robAmount} units of {robType} to my subjects.")
    print(f"SHARE_ROB_FOOD: {master.attributes['name']} shared {robAmount} units of {robType} to {len(master.obey_stats.subjectid)} subjects.")
    return

def share_rob_lost(master:Individual, robAmount:float, robType:str, system:System) -> None:
    if master.obey_stats.subjectid is None or not master.obey_stats.subjectid:
        print("SHARE_LOST_FOOD: no subject, directly lost the rob amount.")
        master.attributes[robType]= master.attributes[robType] - robAmount
        return
    #divide the rob amount to each subject
    for subjectid in master.obey_stats.subjectid:
        subject = system.individuals[subjectid]
        subject.attributes[robType]= subject.attributes[robType] - robAmount/len(master.obey_stats.subjectid)
        subject.memory.append(f"Day {system.time}. I lost {robAmount/len(master.obey_stats.subjectid)} units of {robType} to {master.attributes['name']}.")
    #include the master
    master.attributes[robType] = master.attributes[robType] - robAmount/len(master.obey_stats.subjectid)
    master.memory.append(f"Day {system.time}. I get {robAmount} units of {robType} from my subjects.")
    print(f"SHARE_LOST_FOOD: {master.attributes['name']} got {robAmount} units of {robType} from {len(master.obey_stats.subjectid)} subjects.")
    return

#only allow free individuals to donate
def donate_lost(master:Individual, donateAmount:float, donateType:str, system:System) -> None:
    
    master.attributes[donateType]= master.attributes[donateType] - donateAmount
    return

def donate_gain(master:Individual, donateAmount:float, donateType:str, system:System) -> None:
    
    master.attributes[donateType]= master.attributes[donateType] + donateAmount
    return
    
#Only happen when rob_person rob target and target rebelled
def rob_rebelled(target: Individual, rob_person:Individual, system: System, robType: str)->None:
    #cannot rob self
    if target.attributes['id']==rob_person.attributes['id']:
        print("ROBERROR: cannot rob self.")
        return
    
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
            rob_person.memory.append(f"Day {system.time}. I tried to rob {target.attributes['name']}, who rebelled against me and I lost. I did not gain anything and my social position dropped 1 unit.")
    else:
            victim_memory = ""
            #Rob Person Successfully Rob Target
            lost_food:float=target.attributes['food']
            if robType=='food':
                share_rob_lost(target,lost_food, robType, system)
                share_rob_gain(rob_person,lost_food,robType, system)
                victim_memory=f"I got robbed {lost_food} units of food."
                victor_memory=f"I robbed and gained {lost_food} units of food."
            elif robType=="land":
                if target.attributes['land']>1:
                        share_rob_lost(target,1,robType, system)
                        share_rob_gain(rob_person,1,robType, system)
                        victim_memory=f"I got robbed of 1 land."
                        victor_memory=f"I robbed and gained 1 land."
                else:
                        victim_memory="I have no land to loose."
                        victor_memory="I robbed but he had no land to loose."
            else:
                print(f'Error: rob type does not match anyting. Rob type: {robType}')
            target.attributes['social_position']-=1
            rob_person.attributes['social_position']+=2
            target.memory.append(f"Day {system.time}. {rob_person.attributes['name']} tried to rob me, I rebelled but lost. {victim_memory}. I lost 1 unit of social status.")
            rob_person.memory.append(f"Day {system.time}. I tried to rob {target.attributes['name']}, who rebelled against me but I won. {victor_memory}. I gained 2 units of social status.")

    print("Robbing process finished")
    return

def donate(target: Individual, donate_person:Individual, system: System, donateType: str)->None:
    #cannot donate self
    if target.attributes['id']==donate_person.attributes['id']:
        print("DONATEERROR: cannot donate self.")
        return
    
    donate_perosn_id:int=donate_person.attributes['id']
    if donateType == "food":
        donate_person.memory.append(f"Day {system.time}. I donated to 1 unit fo food to {target.attributes['name']}.")
        target.memory.append(f"Day {system.time}. {donate_person.attributes['name']} donate 1 unit of food to me.")
    elif donateType == "land":
        donate_person.memory.append(f"Day {system.time}. I donated to 1 unit fo land to {target.attributes['name']}.")
        target.memory.append(f"Day {system.time}. {donate_person.attributes['name']} donate 1 unit of land to me.")
    else:
        print(f'Error: rob type does not match anyting. Rob type: {donateType}')
    
    donate_lost(donate_person,1, donateType, system)
    donate_gain(target,1, donateType, system)
    
    print("Donate process finished")
    return


#master punish subject, get his food and land and share it to other subjects except the subject being punished
def punishment(subject:Individual, system:System) -> None:
    if subject.obey_stats.obey_personId==-1:
        print("PUNISHMENTERROR: no master, this should not happen.")
        return
    print(f"PUNISHMENT: {subject.attributes['name']} is punished by {system.individuals[subject.obey_stats.obey_personId].attributes['name']}, all other subjects will share the food and land of {subject.attributes['name']}.")
    master = system.individuals[subject.obey_stats.obey_personId]
    subject.memory.append(f"I was punished by {system.individuals[subject.obey_stats.obey_personId].attributes['name']} because I, as a subject, rob other subject.")
    master.memory.append(f"I punished {subject.attributes['name']} because he, as a subject, rob other subject.")
    #master punish subject, 50% food and 50% land
    food_amount = 0.5 * subject.attributes['food']
    land_amount = 0.5 * subject.attributes['land']
    subject.attributes['food'] -= food_amount
    subject.attributes['land'] -= land_amount
    #share the food and land to other subjects
    for subjectid in master.obey_stats.subjectid:
        if subjectid!=subject.attributes['id']:
            subject.memory.append(f"I got food and land because {subject.attributes['name']} was punished by {master.attributes['name']}, since he robbed other subject.")
            subject = system.individuals[subjectid]
            subject.attributes['food'] += food_amount/(len(master.obey_stats.subjectid)-1)
            subject.attributes['land'] += land_amount/(len(master.obey_stats.subjectid)-1)
    return