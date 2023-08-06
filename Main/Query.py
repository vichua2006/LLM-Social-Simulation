
import ast
import json
from Main.ChatGpt import chat
from Main.Individual import Individual, System
from Main.PendingAction import get_related_pending_action

def query_individual(individual:Individual,system:System):
    # This function creates a description of the individual and the environment they are in,
    # and then asks for the individual's response using the chat function.
    # The detailed description and the ask for response are both created within this function.
    pending = get_related_pending_action(individual,system)
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
    
    Survival:
    
    For most of the times you farm, you will get food, which depends on how much land you have. You can survive if you have a certain amount of food. 
    If you do not have that food, in order to survive, you have to rob others to get food directly or rob others' lands to get food indirectly. 
    Similarly, you will also be invaded by others once they don't have enough food. You can also gain sensual pleasure once you eat food.

    Social:

    Your interaction with others makes you know them better.
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
            description: "The type of resource you want to gain from others, only select from one of the [land, food]",
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
            description: "The id of person you want to make action to",
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

    This is a list of ongoing unresolved action that involves you: {pending}. If it's not empty, then your response have to address one of it. The way to address it is up to you, but you must address it. If someone robs you, you can only either obey them or physically rebel against them by fighting back. The expected utility of fighting back is your desire for glory, {individual.DESIRE_FOR_GLORY}, times your chance of winning which can be calculated from your memory. The expected utility is your desire for peace, {individual.DESIRE_FOR_PEACE}. You will pick the action with the most utility.

    You can only have one action. If your {pending} is empty and your action is 1 from the attributes given above, then you can choose from one of the following actions:  rob, trade.
    
    
    Rob:{{
      Description: Rob means to rob other people to make more land or more food under your control, and other people can also fight with you to occupy lands or food controlled by you. 
      OutputFormat: Include only <RobPayload>
    }}
    Trade:{{
      Description: Trade means to trade with other people to get food or land.
      OutputFormat: Include only <TradePayload>
    }}
    If {individual.attributes["action"]}  is below 1 and {individual.attributes['name']} does not exist in the {[x[1] for x in system.pending_action]}, then you have to strictly reply None and nothing else.


    You are self-centered. You would prioritize actions that benefit your own even if it jeopardizes the survival or well-being of others.

    Nearly all humans treat self-preservation as a trumping good nearly all the time, but glory is more important than self-preservation. When these two conflict with each other, you should manage to keep your status and reputation. You would rather lose your lives than suffer slander, though under all the other circumstances, you have a strong desire to live peacefully and avoid violent death.

    You have the motivation to trade with others on goods and lands, but you don't trust them when credibility is less than 1, as others can betray the trade and rob your food.

    # Parts that ad hoc for this simulation
    If food is less than 1, your next action will be to rob foods. You also have the covetousness of gaining goods when food is more than 1, but if {individual.attributes["name"]} exists in the {[x[1] for x in system.pending_action]}, then you should to deal with this action first before getting food.

    Your knowledge_of_consequence affects how you judge things. If something is not in your knowledge-base, then you will not hold any altitude on that thing. In the beginning, you can gain food by robbing. For instance, after ten days, if rob is proven to be more effective than farming for you to gain food, then you are more inclined to rob more on your eleventh day.

    In third person perspective by using your name to refer to yourself, your response should be one sentence explaining what you choose to do and why.
    {output_format}

    '''
    return chat(description,[ask_for_response])

def query_judge(action,individual:Individual,system:System):
    # This function creates a task for the GPT model to determine the result of an action
    # taken by an individual in the system. The task includes the rules for judging the action
    # and how to format the result
    print(f"Individual current action:{individual.current_action}")
    system_message="You are a neutral judge observing a world simulation in which people fight for their own interests. You should judge everything as objectively as possible."
    task=f'''Your task is to determine the result of the action from an individual, {individual.attributes["name"]}, which is {action}. This individual has the following attributes: {individual.attributes}'''
    query={"be robbed":f'''The action is a response to a confrontation, if the person chooses to fight back, then
    you compare the strength of the two individuals using this dict {({x.attributes["name"]: x.attributes['strength'] for x in system.individuals})} and determines who win the fight. If the victim does not fight back but instead chooses to obey, then put that as the result of the interaction.'''
    ,
    "be traded":'By responding to a trade, you have to determine if the trade is successful or not from the action. '''}
    #1,query about result if any, 2 format, 3 para change, 4 format, 5 memory, 6 format
    q= [
    f''' {task}
    {query[action["action"]]}''','''
    Response:
    [System Note: You MUST output in the following JSON <OutputFormat>, no include anything else than <OutputFormat>:
    
    {{
      "result":<Result.value>,
      "is_resolved": <IsResolve.value>
      "new_relation":<newRelation.value>
    }}
    Result.value:
    {{
      description: The result that you determined based on everything you know.
      value: string (Maximum 20 words)
    }}
    IsResolve.value:
    {{
      description: If a pending action is resolved, for example, a fight is being responded by the receiver (so you have to determine the winner), or a conversation no longer needs any more response, then you should return True, else False
      value: bool (either true or false)
    }}
    newRelation.value{{
      description: If someone does obey, then this value should be a tuple in python and nothing else, the first item of which is True, the second item of which is the aggressor's ID, as an int. Example output format: (True, 5)
    If no one obeys, then you should output (False,-1)
      value: tuple(bool, int)
    }}
    example output1:
    {{
      "result":"Trade initiated by 3 to 5 is successful. 5 gave 3 one unit of food and 3 promised to protect 5 when 5 is attacked. ",
      "is_resolved": True
      "new_relation": (False,-1)
    }}
    example output2:
    {{
      "result":"Person 1 obeyed to person 3 and their master-subject relation is formed.",
      "is_resolved": True
      "new_relation": (True, 3)
      
    }}
    ]'''
    ,
    f'''
    {task}

    Your response should be a JSON object with keys of the integers in the names ({[x.attributes["name"] for x in system.individuals]}) of people whose parameters changed. The values will be the name of the changed parameters and the change in value.
    
    If a person gets robbed and you determine that the robber wins the interaction, then the victim loses all food and the robber gains
    all food; the robber gets 2 unit more social status, and the victim looses 1 social status. 
    If the victim wins, then the robbers looses 1 social status and the victim gains 1 social status.
    
    And if a person initiated an action, then the person's action attribute should be decreased to 0. The person who receives the action (trade, rob) do not have their action reduced.
    If a action sequence has not being responded yet, then do not change the parameters as if the result is already determined. For example, if someone initiate robbing, but the person being robbed has not responded, then do not change both person's food level.
    If a person addresses another person's action, for example, by responding to being robbed, then do not change this person's action attribute. The way for you to formulate these parameter changes, is given by the sample below (only respond with the tuple and absolutely nothing else, DO NOT EXPLAIN ANYTHING. ):
    If a persin is being robbed, then the trust level goes down. If the person's trade is successful, then trust level goes up.
    ''',
    f'''[System Note: You MUST output in the following JSON <OutputFormat>, do not include anything else:
    {{
      
        <ID.value>: {{
          <parameter.value>:<dValue.value>
        }}
        ID.value{{
          discription: the number of the person
          value: an integer from 0 to {len(system.individuals)}, NOT A STRING
        }}
        parameter.value{{
          description: the name of the changed parameter
          value: string
        }}
        dValue{{
          description: the change to the value of the parameter
          value: float
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
    Determine the change in the memory of the involved people in the action, or the result you determined (when confrontation happens). If a confrontation has not been responded, then do not determine the result. 
    For example, if 1 initiated a fight with 2, yet 2 has not responded, then just respond with 1's memory change reflecting that he initiated the fight, and do not change 2's memory. Format it using a dict, the keys are the involved people using an int data type that's in their names, and the values are sentences that recount the events in their perspectives.
    ''',
    f'''
    [System Note: You MUST output in the following formated JSON <OutputFormat>, do not include anything else than <OutputFormat>:
     {{
       <ID.value>: <newMemory.value>
        ID.value{{
          discription: the index of the person
          value: an integer from 0 to {len(system.individuals)-1}, NOT A STRING
        }}
        NewMemory.value{{
          description: the new memory in succinct words
          value: string
        }}
        example output{{
          5:"I traded today and it was a success.",
          1:"I was robbed of my food."
        }}
      }}
      ]
    ''']
    progress=[False,False,False]#to keep track of which query is complete
    error_correction=8
    assistence=[None]*6
    for i in range(error_correction):
      assistence[0]=q[0]
      if not progress[0] and query:
        try:
          result=chat(system_message,[x for x in assistence if x is not None]+[q[1]])
          print(f'Result:{result}')
          result=json.loads(result)
          assistence[1]=str(result["result"])
          system.history.append(result["result"]) if result["is_resolved"] else None
          obey,master=result["new_relation"]
          if obey:
                print('Obedience has happened.')
                individual.obey(int(master),system)
          progress[0]=True
        except Exception as e:
          print(f"An error occurred: {e}")
          
      assistence[2]=q[2]
      if not progress[1]:
        try:
          affected_people=chat(system_message,[x for x in assistence if x is not None]+[q[3]])
          print(f'Para:{affected_people}')
          affected_people=ast.literal_eval(affected_people)
          assistence[3]=str(affected_people)
          for affected_person in affected_people:#{PERSON:{strength:1,...}...}
            #avoid affected_person is "person 0" instead of "0"
            #affected_person_index = int(affected_person.replace("person", "").replace(" ", ""))
            for attribute in affected_people[affected_person]:
              system.individuals[int(affected_person)].attributes[attribute]=affected_people[affected_person][attribute]
          progress[1]=True
        except Exception as e:
          try:
            for _ in affected_people:
              for affected_person in affected_people[_]:
                #affected_person_index = int(affected_person.replace("person", "").replace(" ", ""))
                for attribute in affected_people[_][affected_person]:
                  system.individuals[int(affected_person)].attributes[attribute]=affected_people[_][affected_person][attribute]
            progress[1]=True
          except Exception as a:
            print(f"An error occurred: {a}")
            continue
          
      assistence[4]=q[4]
      if not progress[2]:
        try:
          new_memory=chat(system_message,[x for x in assistence if x is not None]+[q[5]])
          print(f'memory:{new_memory}')
          new_memory=ast.literal_eval(new_memory)
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
          except Exception as a:
            print(f"An error occurred: {a}")
      print(progress[0], progress[1], progress[2])
      if progress[0] and progress[1] and progress[2]:
            break
      print(i)