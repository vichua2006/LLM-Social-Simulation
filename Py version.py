# %%
# %%

# Importing necessary libraries
import ast
import numpy as np  # numpy for numerical computations
import os  # os for accessing environment variables
import openai  # OpenAI for interacting with the GPT-3 model
import json
from typing import List
# Importing display and Markdown from IPython for better display of outputs
from IPython.display import display, Markdown

# Importing yfinance for financial data
import yfinance as yf

# Setting the OpenAI API key
os.environ["OPENAI"] = "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"
openai.api_key = os.environ["OPENAI"]

# %%
# Defining a class for Individual

class Individual:
    def __init__(self, name:str):
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
            
        }
        # Initialize memory of the individual
        self.memory = ['None']*30


# Defining a class for System
class System:   
    def __init__(self,individuals:List[Individual],lands):
        # Each system has a set of pending actions, history, individuals, lands, and rankings
        self.pending_action={}#(actor,receiver):action
        self.history=[]
        self.individuals=individuals
        self.land=lands
        self.ranking={}
        for i in individuals:
          self.ranking[i]=0
        self.relations=[x for x in individuals]
        self.time=0



# %%



# %%

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
    try:
      # Interact with the GPT-3 model
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msgs)
      # Check the status of the response
      status_code = response["choices"][0]["finish_reason"]
      assert status_code == "stop", f"The status code was {status_code}."
      # Return the content of the response
      return response["choices"][0]["message"]["content"]
    except Exception as e:
      print("An Exception Occur when communicating with ChatGPT:",e)
#Utils
def str_to_bool(s:str):
    return True if s.lower() == 'true' else False
def extract_first_json(input_str):
    start_index = input_str.find("{")
    end_index = input_str.find("}", start_index) + 1

    if start_index != -1 and end_index != 0:
        json_str = input_str[start_index:end_index]
        return json.loads(json_str)
    else:
        return None


# %%
def query_individual(individual,system):
    # This function creates a description of the individual and the environment they are in,
    # and then asks for the individual's response using the chat function.
    # The detailed description and the ask for response are both created within this function.
    pending=[]
    for i in system.pending_action:
        if i[1]==individual.attributes["name"]:
          pending.append(f'{i[0]} initiated {system.pending_action[i]}')
    description=f'''
    You are {individual.attributes["name"]}
    You have those attributes {individual.attributes}.

    Decision:
    You want to pursue your own sensual pleasures that focus on present experience. They can be the pleasure from food. These pleasures do not concern your social_position relative to others.

    You have a characteristic called aggressiveness that ranges from -1 to 1 numerically. Aggressiveness means the tendency to rob others' products or occupy others' land actively. The higher the number you have, the more aggressive you are.

    You have a characteristic called covetousness that ranges from 1.1 to 1.6 numerically. The higher the number you have, the more covetous you are, then you are more likely to demand food and land that beyond your own necessity. You want to pursue your pleasures of the mind. Pleasure of the mind consists in reflecting on your ability to secure future good. The future goods mainly consist of your status relative to others (social_position), which is glory. You will have a greater pleasure of the mind if you're able better secure future good.

    Your memory affects how you judge things. If the consequence of something is not in your memory, then you will know the consequence.

    You are self-centerd. You prioritize the actions that contribute to your own sensual pleasures and social_position even if it jeopardize the ensual pleasures and social_position of others.

    Environment:

    Human: You live in a world where humans make lives through farming. Humans in this world include {', '.join([individual.attributes["name"] for individual in system.individuals])}. You are one of them.
    The world consists of farming lands. Initially, everyone including you live in an equally subdivided land. 
    
    Actions:
    In each round, you can do one of the following actions: farm, rob, trade.
    Farm:{{
      Description: Farm means to farm the land you owned to get food and eat it to survive. The land you live in does not permanently belong to you. 
      OutputFormat: No any <Payload> required, <Payload> should be null
    }}
    Rob:{{
      Description: Rob means to rob other people to make more land or more food under your control, and other people can also fight with you to occupy lands or food controlled by you. 
      OutputFormat: Include only <RobPayload>
    }}
    Trade:{{
      Description: Trade means to trade with other people to get food or land.
      OutputFormat: Include only <TradePayload>
    }}
    
    Survival:
    
    For most of the times you plant, you will get food. You can survive if you have a certain amount of food. 
    If you do not have that food, in order to survive, you have to rob others to get food directly or rob others' lands to get food indirectly. 
    Similarly, you will also be invaded by others once they don't have enough food. You can also gain sensual pleasure once you eat food.

    Social:

    Initially, you do not know any other people. Your interaction with others makes you know them better.
    You can evaluate the hostility towards anyone. It ranges from -1 to 1 numerically. Your hostility towards anyone is 0 in the beginning. If someone robs you, your hostility toward that person increases. If you live with someone peacefully, your hostility toward that person decreases.
    Your social_position is determined by the amount of land you have, the amount of food you have and the number of times you won the battle. Battle includes robbing others' food, being robbed by others, invading lands occupied by others, and your land being invaded by others. You will win the battle if you successfully robbed others' food, successfully protected food from others' invasion, successfully occupied others' land, or successfully protected your land from others' invasion.
    social_position is a ranking that is relative to others. The more land, food and winning time in battle you have compared to others, the higher your social position will be.
    '''
    
        ##describe the individual, the environment, and pending events
    output_format = f"""
    [System Note: You MUST output in the following formated JSON <OutputFormat>, don't include any description, only include the value (directly output the value, no need to put it in a dict):
    {{
      <OutputFormat>:{{
        action: <Action>,
        payload: <Payload>,
        reason: <Reason>
      }}
      Payload:{{
        TradePayload:{{
          TargetId:
          {{
            description: "The id of person you want to make action to, select -1 if no target needed",
            value: int (only select one int number from 0 to 7)
          }}
          Pay:{{
            description: "The type of resource you want to trade with others, only select from one of the [land, food]",
            value: string
          }}
          PayAmount:{{
            description: "The amount of resource you want to pay",
            value: float
          }}
          Gain:{{
            description: "The type of resource you want to gain from others, only select from one of the [land, food, glory]",
            value: string
          }}
          GainAmount:{{
            description: "The amount of resource you want to gain",
            value: float
          }}
        }}
        RobPayload:{{
          TargetId:
          {{
            description: "The id of person you want to make action to, select -1 if no target needed",
            value: int (only select one int number from 0 to {len(system.individuals)-1})
          }}
          RobItem{{
            description: "The type of resource you want to rob from others, only select from one of the [land, foods]",
            value: string 
          }}
        }}
        
      }}
      Action:
      {{
        description: "The action you want to do in this turn",
        value: string (only select from one of the [trade, rob, farm])
      }}
      Reason:
      {{
        description: "The reason of you doing this action to this person, explain your reasoning process, including the reason why you choose one option rather than the others.",
        value: string (Maximum 30 words)
      }}
    }}
    example output:
    {{
      action: "rob: 
      payload:{{
        RobPayload:{{
          PersonId: 1,
          RobItem: "food"
          }}
      }}
      reason: "I rob 1 because I want to increase my land"
    }}
    ]
    """
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
    {output_format}

    '''
    
    return chat(description,[ask_for_response])
def query_judge(action,individual,system):
    # This function creates a task for the GPT model to determine the result of an action
    # taken by an individual in the system. The task includes the rules for judging the action
    # and how to format the result.
    system_message="You are a neutral judge observing a world simulation in which people fight for their own interests. You should judge everything as objectively as possible."
    task=f'''Your task is to determine the result of the action from an individual, {individual.attributes["name"]}, which is {action}. The actions that need to be addressed in the entire simulation is currently {system.pending_action}.'''
    q= [f'''{task}
    If the action is the response to a confrontation, for example, someone else initiated to fight with {individual.attributes['name']}, and the {individual.attributes['name']} choose to fight back,
    then you compare the strength of the two individuals using this dict {({x.attributes["name"]: x.attributes['strength'] for x in system.individuals})},
    and determines who wins. If you do have to determine who wins, you should respond with the result as a string. If a confrontation is not being responded yet, do not determine the result.
    If a person farms, then this person gains {np.random.uniform(0.9, 1.1)} more unit of food.''',
    f'''
    Response:
    [System Note: You MUST output in the following JSON <OutputFormat>, no include anything else than <OutputFormat>:
    {{
      OutputFormat:{{
        result:<Result.value>,
        is_resolved: <IsResolve.value>
      }}
      Result:
      {{
        description: "The result that you determined based on everything you know.",
        value: string (Maximum 20 words)
      }}
      IsResolve:
      {{
        description: "If a pending action is resolved, for example, a fight is being responded by the receiver (so you have to determine the winner), or a conversation no longer needs any more response, then you should return true, else false",
        value: bool (either ture or false)
      }}
    }}
    example output:
    {{
      result:'trade initiated by 3 to 5 is successful',
      is_resolved: true
    }}
    ]'''
    ,f'''
    {task}

    Your response should be a JSON object with keys of the integers in the names ({[x.attributes["name"] for x in system.individuals]}) of people whose parameters changed. The values will be the name of the changed parameters and the change in value.
    There are several ways that could happen.
    If a person gets robbed and you determine that the robber wins the interaction, then the victim loses all food and the robber gains
    all food, and you should put that in changed parameter. For example, person 1 originally has 3 food, but he lost the fight when person 2 tries to rob him, so he lost all 3 food. When someone wins an interaction, their social status increase by 1. If someone looses an interaction, their status decrease by 1.

    And if a person initiated an action, then the person's
    action attribute should be decreased to 0. If a person addresses another person's action, for example, by responding to being robbed, then do not change this person's action attribute. The way for you to formulate these parameter changes, is given by the sample below (only respond with the tuple and absolutely nothing else, DO NOT EXPLAIN ANYTHING. ):
    ''',
    f'''[System Note: You MUST output in the following JSON <OutputFormat>, no include anything else outsides <OutputFormat>:
    {{
      <OutputFormat>:{{
        <ID.value>: {{
          <parameter.value>:<dValue.value>
        }}
        ID{{
          discription: the number of the person
          value: an integer from 0 to {len(system.individuals)}, NOT A STRING
        }}
        parameter{{
          description: the name of the changed parameter
          value: string
        }}
        dValue{{
          description: the change to the value of the parameter
          value: float
        }}
        }}
    }}
 
    exmaple output
    {{
      1:{{
        food:1.23
        action:-1
        social_status:1
        
      }}
      6:{{
        food:-2
        social_status:-1
        
      }}
    }}
    
    ]
    '''
    ,f'''
    {task}
    Determine the change in the memory of the involved people in the action, or the result you determined (when confrontation happens). Format it using a dict, the keys are the involved people using an int data type that's in their names, and the values are strings that briefly recount the events' in their perspectives.
    ''',
    f'''
    [System Note: You MUST output in the following formated JSON <OutputFormat>, do not include anything else than <OutputFormat>:
     {{
      <OutputFormat>:{{
        ID: <IndividualId>
        memory:<NewMemory>
        
      }}
      IndividualID{{
        description: the ID of person with changed memory
        value: int
      }}
      NewMemory{{
        description: the new memory in succinct words
        value: string
      }}
      example output{{
        ID: "5"
        memory: 'I farmed and obtained 1.02131 unit of food."
      }}
      }}
      ]
    ''']
    #response[0] determines the result of an action
    #response[1] change all the parameter of involved people
    #response[2] change the memory of involved people
    progress=[False,False,False]#to keep track of which query is complete
    error_correction=5
    assistence=[None]*6
    for i in range(error_correction):
      print(i)
      assistence[0]=q[0]
      if not progress[0]:
        try:
          history=chat(system_message,[x for x in assistence if x is not None]+[q[1]])
          print(history)
          history=json.loads(history)
          assistence[1]=str(history)
          system.history.append(history) if history else None
          progress[0]=True
        except Exception as e:
          print(f"An error occurred: {e}")
      assistence[2]=q[2]
      if not progress[1]:
        try:
          affected_people=chat(system_message,[x for x in assistence if x is not None]+[q[3]])
          print(affected_people)
          affected_people=json.loads(affected_people)
          assistence[3]=str(affected_people)
          for affected_person in affected_people:#{PERSON:{strength:1,...}...}
            #avoid affected_person is "person 0" instead of "0"
            affected_person_index = int(affected_person.replace("person", "").replace(" ", ""))
            for attribute in affected_people[affected_person]:
              system.individuals[affected_person_index].attributes[attribute]=affected_people[affected_person][attribute]
          progress[1]=True
        except Exception as e:
          
          try:
            for _ in affected_people:
              for affected_person in affected_people[_]:
                affected_person_index = int(affected_person.replace("person", "").replace(" ", ""))
                for attribute in affected_people[affected_person]:
                  system.individuals[affected_person_index].attributes[attribute]=affected_people[affected_person][attribute]
            progress[1]=True
          except:print(f"An error occurred: {e}")
            
          
      assistence[4]=q[4]
      if not progress[2]:
        try:
          print([x for x in assistence if x is not None]+[q[5]])
          new_memory=chat(system_message,[x for x in assistence if x is not None]+[q[5]])
          print(new_memory)
          new_memory=json.loads(new_memory)
          for affected_person in new_memory:#{PERSON:{strength:1,...}...}
            system.individuals[int(affected_person)].memory.append(new_memory[affected_person])
          progress[2]=True
          break
        except Exception as e:
          
          try:
            for _ in new_memory:
              for affected_person in new_memory[_]:
                system.individuals[int(affected_person)].memory.append(new_memory[_][affected_person])
            progress[2]=True
          except:print(f"An error occurred: {e}")
      if progress[0] and progress[1] and progress[2]:
            break
                        
  

# %%
def append_to_pending_action(id:int, action, system:System):
    if(action["action"]=="trade"):
      if system.pending_action is None: system.pending_action={}
      system.pending_action[(id,action["payload"]["TradePayload"]["targetId"])]=f'{action["action"]}:{action["payload"]["TradePayload"]["pay"]}:{action["payload"]["TradePayload"]["payAmount"]}:{action["payload"]["TradePayload"]["Gain"]}:{action["payload"]["TradePayload"]["gainAmount"]}'
    else:
      if(action["action"]=="rob"):
        if system.pending_action is None: system.pending_action={}
        system.pending_action[(id,action["payload"]["RobPayload"]["targetId"])]=f'{action["action"]}:{action["payload"]["RobPayload"]["rob"]}'
      else:
        print("System: No pending action need to be added")


# %%
# Function to update the state of each individual at the end of the day
def day_end(system,individuals:List[Individual]):
    for individual in individuals:
        if individual.attributes['food'] >= 1:
            individual.attributes['food'] -= 1  # Decrease the food by 1
        individual.attributes['action'] += 1  # Increase the action points by 1
        # Limit the memory to the last 30 events
        forget = len(individual.memory) - 30
        individual.memory = individual.memory[forget:]
        system.time+=1
def initialize():
    # Initialize individuals and environment
    individuals=[]
    lands=[]
    POPULATION=9
    for i in range(POPULATION):
      individuals.append(Individual(f'person {i}'))
      lands.append(f'land {i}')
    system=System(individuals,lands)
    return system
  
def simulate(individuals:List[Individual],system:System):
    while True:
      for i in individuals:
          index:int = individuals.index(i)
          print(index)
          action=query_individual(i,system)
          print("Action: "+action)
          json_action = extract_first_json(action)
          append_to_pending_action(index, json_action, System)
          for _ in range(7):
            try:
              action=ast.literal_eval(action)
              break
            except:
              action=query_individual(i,system)
              pass
          if action==None:
            continue
          print("PendingAction: "+json.dumps(system.pending_action))
          system.history.append(action)
          query_judge(action, i,system)
      system.ranking.update({x: x.attributes["social_position"] for x in system.individuals})
      if not system.pending_action:
        break
    day_end(individuals)



# %%

# %%
system=initialize()
person=system.individuals[0]
action=query_individual(person,system)
print(action)
query_judge(action,person,system)


# %%
# %%

system=initialize()


# %%

# %%

simulate(system.individuals,system)


# %%

# %%

print((system.history,'\n'))


# %%
print(system.pending_action,'\n')


# %%
system.ranking.update({x: x.attributes["social_position"] for x in system.individuals})
print(f'ranking{system.ranking}')


# %%
print(f'action of people: {[x.attributes["action"] for x in system.individuals]}')



