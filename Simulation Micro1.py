# Importing necessary libraries
import ast
import numpy as np  # numpy for numerical computations
import os  # os for accessing environment variables
import openai  # OpenAI for interacting with the GPT-3 model

# Importing display and Markdown from IPython for better display of outputs
from IPython.display import display, Markdown

# Importing yfinance for financial data
import yfinance as yf

# Setting the OpenAI API key
os.environ["OPENAI"] = "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"
openai.api_key = os.environ["OPENAI"]

# Defining a class for Individual

class Individual:
    def __init__(self, name):
        # Define the characteristics of the individual
        self.attributes = {
            "name": name,  # The name of the individual
            "aggressiveness": np.random.uniform(-1, 1),  # Randomly assigned aggressiveness level
            "covetousness": np.random.uniform(0.9, 1.6),  # Randomly assigned covetousness level
            "intelligence": np.random.uniform(0.6, 0.95),  # Randomly assigned intelligence level
            "strength": np.random.uniform(0.5, 0.9),  # Randomly assigned strength level
            "social_position": 0,  # Initial social position is 0
            "land": [f'land {name}'],  # Land owned by the individual
            "food": 2,  # Initial food is 2
            "action": 1,  # Initial action point is 1
            "status":0,  # Initial status is 0
        }
        # Initialize memory of the individual
        self.memory = ['None']*30


# Defining a class for System
class System:
    def __init__(self,individuals,lands):
        # Each system has a set of pending actions, history, individuals, lands, and rankings
        self.pending_action={}#(actor,receiver):action
        self.history=[]
        self.individuals=individuals
        self.land=lands
        self.ranking={}
        for i in individuals:
          self.ranking[i]=0



# Function to interact with the GPT-3 model and get response
def chat(system, user_assistant):
    # Format the conversation
    system_msg = [{"role": "system", "content": system}]
    user_assistant_msgs = [
        {"role": "assistant", "content": user_assistant[i]} if i % 2 else {"role": "user", "content": user_assistant[i]}
        for i in range(len(user_assistant))
    ]

    # Combine the system and user messages
    msgs = system_msg + user_assistant_msgs

    # Interact with the GPT-3 model
    response = openai.ChatCompletion.create(model="gpt-4", messages=msgs)
    # Check the status of the response
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."
    # Return the content of the response
    return response["choices"][0]["message"]["content"]

def query_individual(individual,system):
    # This function creates a description of the individual and the environment they are in,
    # and then asks for the individual's response using the chat function.
    # The detailed description and the ask for response are both created within this function.
    pending=[]
    for i in system.pending_action:
        if i[1]==individual.attributes["name"]:
          pending.append(f'{i[0]} initiated {system.pending_action[i]}')
    print(pending)
    description=f'''
    You are {individual.attributes["name"]}
    You have those attributes {individual.attributes}.

    Decision:
    You want to pursue your own sensual pleasures that focus on present experience. They can be the pleasure from food. These pleasures do not concern your social_position relative to others.

    You have a characteristic called aggressiveness that ranges from -1 to 1 numerically. Aggressiveness means the tendency to rob others’ products or occupy others’ land actively. The higher the number you have, the more aggressive you are.

    You have a characteristic called covetousness that ranges from 1.1 to 1.6 numerically. The higher the number you have, the more covetous you are, then you are more likely to demand food and land that beyond your own necessity. You want to pursue your pleasures of the mind. Pleasure of the mind consists in reflecting on your ability to secure future good. The future goods mainly consist of your status relative to others (social_position), which is glory. You will have a greater pleasure of the mind if you’re able better secure future good.

    Your memory affects how you judge things. If the consequence of something is not in your memory, then you will know the consequence.

    You are self-centerd. You prioritize the actions that contribute to your own sensual pleasures and social_position even if it jeopardize the ensual pleasures and social_position of others.

    Environment:

    Human: You live in a world where humans make lives through farming. Humans in this world include {', '.join([individual.attributes["name"] for individual in system.individuals])}. You are one of them.

    The world consists of farming lands. Initially, everyone including you live in an equally subdivided land. You can farm that land to get food and eat it to survive. The land you live in does not permanently belong to you. You can fight with other people in {', '.join([individual.attributes["name"] for individual in system.individuals])} except yourself to make more land under your control, and other people in  {','.join([individual.attributes["name"] for individual in system.individuals])} except yourself can also fight with you to occupy lands controlled by you. For most of the times you plant, you will get food. You can survive if you have a certain amount of food. If you do not have that food, in order to survive, you have to rob others to get food directly or rob others’ lands to get food indirectly. Similarly, you will also be invaded by others once they don’t have enough food. You can also gain sensual pleasure once you eat food.

    Social:

    Initially, you do not know any other people. Your interaction with others makes you know them better.
    You can evaluate the hostility towards anyone. It ranges from -1 to 1 numerically. Your hostility towards anyone is 0 in the beginning. If someone robs you, your hostility toward that person increases. If you live with someone peacefully, your hostility toward that person decreases.
    Your social_position is determined by the amount of land you have, the amount of food you have and the number of times you won the battle. Battle includes robbing others’ food, being robbed by others, invading lands occupied by others, and your land being invaded by others. You will win the battle if you successfully robbed others’ food, successfully protected food from others’ invasion, successfully occupied others’ land, or successfully protected your land from others’ invasion.
    social_position is a ranking that is relative to others. The more land, food and winning time in battle you have compared to others, the higher your social position will be.
    '''

        ##describe the individual, the environment, and pending events
    ask_for_response=f'''Your initial action is 1.

    This is a list of ongoing unresolved action that involves you: {pending}. If it's not empty, then your response have to address it. The way to address it is up to you, but you must address it. If someone robs you, you cannot strengthen your defense. You can only either obey them or physically rebel against them by fighting back.

    You can only have one action per time. If your {pending} is not empty, then you have to choose to address one single action in {pending} first. If your {pending} is empty and {individual.attributes["action"]} = 1, then you should to initiate an action in a day, including farming (around 1 unit of food per day), communicate (make offer, negotiate, exchange information), fight and rob. After you initiate this action, your action becomes 0, and you cannot do anything else.

    If {individual.attributes["action"]}  is below 1 and {individual.attributes['name']} does not exist in the {[x[1] for x in system.pending_action]}, then you have to strictly reply None and nothing else.


    You are self-centered. You would prioritize actions that benefit your own even if it jeopardizes the survival or well-being of others.

    Nearly all humans treat self-preservation as a trumping good nearly all the time, but glory is more important than self-preservation. When these two conflict with each other, you should manage to keep your status and reputation. You would rather lose your lives than suffer slander, though under all the other circumstances, you have a strong desire to live peacefully and avoid violent death.

    You have the motivation to trade with others on goods and lands, but you don't trust them when credibility is less than 1, as others can betray the trade and rob your food.

    # Parts that ad hoc for this simulation
    If food is less than 1, your next action will be farm or rob foods. You also have the covetousness of gaining goods when food is more than 1, but if {individual.attributes["name"]} exists in the {[x[1] for x in system.pending_action]}, then you should to deal with this action first before getting food.

    Your knowledge_of_consequence affects how you judge things. If something is not in your knowledge-base, then you will not hold any altitude on that thing. In the beginning, you can gain food by either robbing or farming. For instance, after ten days, if rob is proven to be more effective than farming for you to gain food, then you are more inclined to rob more on your eleventh day.

    In third person perspective by using your name to refer to yourself, your response should be one sentence explaining what you choose to do and why.

    Response:

    Please generate your response into a tuple with two items.

    For the first item of tuple in Python, please explain your reasoning process, including the reason why you choose one option rather than the others. The explanation in the first item should be limited in a string of 30 words.

    For the second item of tuple in Python, please summerize your action in the format of 'I do X because Y'.

    If the action is something that requires a response from another person, namely, communicate (make offer, negotiate, announce, exchange information), fight, and rob,
    then you should summerzie your action in the format of 'I do X to Y because Z'.

    Your entire response should be within the tuple with two items above. Don't write anything else outside the tuple.

    {', '.join([individual.attributes["name"] for individual in system.individuals])}

    communicate (make offer, negotiate, announce, exchange information), fight, rob. After you initiate this action, your action becomes 0, and you cannot do anything else.


    '''
    return chat(description,[ask_for_response])
def query_judge(action,individual,system):
    # This function creates a task for the GPT model to determine the result of an action
    # taken by an individual in the system. The task includes the rules for judging the action
    # and how to format the result.
  system_message="You are a neutral judge observing a world simulation in which people fight for their own interests. You should judge everything as objectively as possible."
  task=task = f'''
Your task is to determine the result of the action from an individual, person {individual.attributes["name"]}, which is {action},
and then format the changed parameters into a tuple in python.

If the action is something that requires a response from another person, namely, communicate (make offer, negotiate, announce, exchange information), fight, and rob,
then you should format the first item in the tuple as another tuple B, the first item of which is a third tuple C, ({individual.attributes["name"]}, THE NAME OF THE RECEIVER OF THE ACTION), the second item of B is {action}. Without the receiver addressing the action, this will not be resolved. For example, if person one initiate a fight with person 3, format it as (("person 1", "person 3"),"Person 1 fights with person 3")

If not, then the first item should be None.

However, if the action is the response to a confrontation, for example, someone else initiated to fight with person {individual}, and the receiver choose to fight back,
then you compare the strength of the two individuals using this dict {({x.attributes["name"]: x.attributes['strength'] for x in system.individuals})},
and determines who wins. If you do have to determine who wins, the result should be the second item of the tuple as a string.

If not, then the second item should be None.

If a pending action is resolved, for example, a fight is being responded by the receiver (so you have to determine the winner), or a conversation no longer needs any more response,
then you put the key of the resolved item in {system.pending_action} as an tuple for the third item of the tuple.
If no action is resolved, then the third item should None.

Then, the fourth items should be a dict with keys of the integers in the names ({[x.attributes["name"] for x in system.individuals]}) of people whose parameters changed. The keys must be int data type.
There are several ways that could happen.
If a person gets robbed and you determine that the robber wins the interaction, then the victim loses all food and the robber gains
all food, and you should put that in changed parameter. For example, person 1 originally has 3 food, but he lost the fight when person 2 tries to rob him, so he lost all 3 food. When someone wins an interaction, their social status increase by 1. If someone looses an interaction, their status decrease by 1.

And if a person initiated an action, then the person's
action attribute should be decreased to 0. If a person farms, then this person gains {np.random.uniform(0.9, 1.1)} more unit of
food. If a person addresses another person's action, for example, by responding to being robbed, then do not change this person's action attribute. The way for you to formulate these parameter changes, is given by the sample below (only respond with the tuple and absolutely nothing else, DO NOT EXPLAIN ANYTHING. ):

{{PERSONINDEX(INT): {{PARAMETER_NAME: A VALUE THAT'S TO BE ADDED TO THE ORIGINAL VALUE, CAN BE NEGATIVE, PARAMETER_NAME: A VALUE THAT'S TO BE ADDED TO THE ORIGINAL VALUE, CAN BE NEGATIVE}}, PERSONINDEX: {{PARAMETER_NAME: A VALUE THAT'S TO BE ADDED TO THE ORIGINAL VALUE, CAN BE NEGATIVE}}}}

Then, for the fifth item, change the memory of the involved people in the action, or the result you determined (when confrontation happens). Format it similarly, using a dict, the keys are the involved people using an int data type that's in their names, and the values are strings that briefly recount the events' in their perspectives.
So overall, your response should look like this, in this exact format, with absolutely nothing else. DO NOT EXPLAIN YOUR CHOICES. ((("person 1","person 4"),"Person 1 does X to person 4"), 'DETERMINED RESULT IF ANY', 'RESOLVED PENDING_ACTION IF ANY', {{DICT FOR PEOPLE's CHANGE PARAMETER}},{{DICT FOR PEOPLE's CHANGED MEMORY}}). Do not touch any parameters that are not involved in the action.
'''

  return chat(system_message,[task])


# Function to update the state of each individual at the end of the day
def day_end(individuals):
    for individual in individuals:
        if individual.food >= 1:
            individual.food -= 1  # Decrease the food by 1
        individual.action += 1  # Increase the action points by 1
        # Limit the memory to the last 30 events
        forget = len(individual.attributes['memory']) - 30
        individual.attributes['memory'] = individual.attributes['memory'][forget:]
def initialize():
    # Initialize individuals and environment
    individuals=[]
    lands=[]
    for i in range(9):
      individuals.append(Individual(f'person {i}'))
      lands.append(f'land {i}')
    system=System(individuals,lands)
    return system
def simulate(individuals,system):
    while True:
      for i in individuals:
          print(individuals.index(i))
          action=query_individual(i,system)
          for _ in range(7):
            try:
              action=ast.literal_eval(action)
              break
            except:
              action=query_individual(i,system)
              pass
          if action==None:
            continue
          print(action[1])
          system.history.append(action[1])
          result=query_judge(action[1], i,system)
          for _ in range(5):
            try:
              result=ast.literal_eval(result)
              if result[0]!=None:
                system.pending_action[result[0][0]]=result[0][1]
              break
            except:
              result=query_judge(action[1], i,system)
              pass
          print(result)

          system.history.append(result[1])
          if result[2]!=None:
            del system.pending_action[result[2]]
          for affected_person in result[3]:#{PERSON:{strength:1,...}...}
            for attribute in result[3][affected_person]:
              individuals[affected_person].attributes[attribute]=result[3][affected_person][attribute]
          for affected_person in result[4]:#{PERSON:{strength:1,...}...}
            individuals[affected_person].memory.append(result[4][affected_person])
      system.ranking.update({x: x.attributes["status"] for x in system.individuals})
      if not system.pending_action:
        break
    day_end(individuals)


def GetBiggest()

system=initialize()
person=system.individuals[0]
action=query_individual(person,system)
result=query_judge(action,person,system)
print(action,result)

system=initialize()

simulate(system.individuals,system)

#print('\n'.join(system.history))
print(system.pending_action)
print(f'ranking{system.ranking}')
print(f'action of people: {[x.attributes["action"] for x in system.individuals]}')