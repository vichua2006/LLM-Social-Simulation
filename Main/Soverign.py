interval_of_properity=["poor","medium income","affluent"]# to be swapped with two touple integer value.
society_description=None #Describe the society and the things going on. The mechanisms of each actions. how much one consumes, how much one produce. How much people. General context can include the contextual prompts we’ve written before, just adding the sovereign and other parts.
equality_purpose_statement="You are a wise king who cares for the people, and you want to promote equity in your realm of control so that it can be a just society where each person leads a life of equality and respect."
food_std,food_mean,land_std,land_mean=None#WIP
fixed_context=f'''You are the king of the society. {society_description}
{equality_purpose_statement}
Society's food Mean {"[{},{})".format(interval_of_properity[0][0],interval_of_properity[0][1])}: poor
Society's food Mean {"[{},{})".format(interval_of_properity[1][0],interval_of_properity[2][1])}: medium
Society's food Mean {"[{},{})".format(interval_of_properity[2][0],interval_of_properity[2][1])}: affluent
If someone's food is below {food_mean}(mean) - 2*{food_std}(standard deviation)={food_mean-2*food_std}, then this person is relatively poor, and might be ashamed of it.
If someone's food is above {food_mean}(mean) + 2*{food_std}(standard deviation)={food_mean+2*food_std}, then this person is relatively wealthy and might be proud of it.

Without land, individual cannot farm and produce food to survive. 
If someone's land ownership is below {land_mean}(mean) - 2*{land_std}(standard deviation)={land_mean-2*land_std}, then this person is relatively poor, and might be ashamed of it.
If someone's land ownership is above {land_mean}(mean) + 2*{land_std}(standard deviation)={land_mean+2*land_std}, then this person is relatively wealthy and might be proud of it.
'''
individual_wealth={} # dict{name:wealth}, make it sorted, descending order.
enumerate_wealth=""#WIP
for i in individual_wealth:enumerate_wealth+='{} has {} in farmer currency.'.format(i,individual_wealth[i])
gdp=sum(individual_wealth.items())
gini=None#WIP
person_change_in_wealth={}#WIP
enumerate_change=""
for i in person_change_in_wealth:
    changed="dropped" if person_change_in_wealth[i]<0 else "increased"
    enumerate_change+='{}\'s wealth has {} by {}.'.format(i,changed,person_change_in_wealth[i])
dGDP=None#WIP
mean_production=None#WIP
rate_of_activities=""#WIP
goods_distribution=""#WIP
conversations=""#WIP
live_data=f'''LIVE DATA: The individuals wealth listed below in descending order along with their change in wealth:{enumerate_wealth, enumerate_change }

Collective wealth GDP is {gdp}.
GINI coefficient:{gini}.
Collective change in wealth:{dGDP}
Daily average household production: {mean_production}.

Rates of activities:{rate_of_activities}.
Distribution of goods production: {goods_distribution}.
Conversations:{conversations}
'''
policy_explanation=""#Explain what policies are possible, formatting, etc. Where you insert this paragraph can change based on how function call is done.
query=f'''
Q: You are about to make policies. You can use any modern analysis tools you know of and any number of them, to make a policy that you think will help you achieve you objective.{policy_explanation} What is your policy?
A: Let's think step by step.
'''