
import ast
import json
from Main.AIAction import AIActionType
from Main.ChatGpt import chat
from Main.Individual import Individual, System


def query_individual(individual:Individual,system:System,response_action):
    # This function creates a description of the individual and the environment they are in,
    # and then asks for the individual's response using the chat function.
    # The detailed description and the ask for response are both created within this function.
    print(f"Responding to:{response_action}")
    is_subject=individual.obey_stats.obey_personId!=-1
    is_master=individual.obey_stats.subject
    obedience=f'''You have obeyed to this person: Person {individual.obey_stats.obey_personId}. You have to always obey his actions, and you cannot initiate any action against him. Since you obeyed, you are now part of the group of people who also obeyed him, if any, they are {system.individuals[individual.obey_stats.obey_personId].obey_stats.subject}. If your action targets another person, it can only be a person within this group. You are familiar with everyone in this group. Your familiarity of people not in this group depends on your memory.You have your farming land protected by your master. If 
    someone in the commonwealth robs your food or your land, you 
    master will punish the robber. If someone in your group 
    trades with you but defaulted, your master will punish that 
    defaulter.But if your master want, they can take any amount 
    of your land or food from you, and you have no right to 
    disobey. 
    When others outside your commonwealth robs your master 
    and your master obeyed to them, the one your original master 
    obeyed to will be your new master. Now you obey to your new 
    master, and you have no obedience with your old master.'''
    master=f'''These people have obeyed to your invasion: {[f"Person"+str(i) for i in individual.obey_stats.subject]}, whom have become your subjects. You can trade or rob them knowning that they will only accept.
    You are the master of everyone who obeyed you before. You know every one of your subjects in your subjects well. Since you are the master of all of them, all their property including land and food belongs to you. When others rob your subjects, you should project them since they are your property.
    If you obey anyone, the one robbing you 
    now becomes your master and all the subjects of your 
    commonwealth. Besides, you no longer be the master of all the 
    subjects you have in your commonwealth. All of the subjects 
    you once had and you are now the subject of the one you obey 
    to.'''
    general_description=f'''
    You are {individual.attributes["name"]}
    You have those attributes {individual.attributes}.
    You have memory:{individual.memory}
    Environment: You live in a world with other people. Humans in this world include {', '.join([individual.attributes["name"] for individual in
    system.individuals])}. You are one of them.
    Currently, the amount of food each person has is: {[{i.attributes['name']:i.attributes['food'] for i in system.individuals}]}
    The amount of land each person has is:{[{i.attributes['name']:i.attributes['land'] for i in system.individuals}]}
    Survival: You can survive if you have 1 unit of food. You can 
    also gain sensual pleasure once you eat food.
    Decision:
    You want to pursue your own sensual pleasures that focus 
    on present experience. They can be the pleasure from food. 
    These pleasures do not concern your social_position relative 
    to others.
    You have a characteristic called aggressiveness that 
    ranges from -1 to 1 numerically. Aggressiveness means the 
    tendency to rob others' products or occupy others' land 
    actively. The higher the number you have, the more aggressive 
    you are.
    You have a characteristic called covetousness that ranges 
    from 1.1 to 1.6 numerically. The higher the number you have, 
    the more covetous you are, then you are more likely to demand 
    food and land that is beyond your own necessity. You want to 
    pursue your pleasures of the mind. Pleasure of the mind 
    consists in reflecting on your ability to secure future good. 
    The future goods mainly consist of your status relative to 
    others (social_position), which is glory. You will have a 
    greater pleasure of the mind if you're able better secure 
    future good.
    Your memory affects how you judge things. If the 
    consequence of something is not in your memory, then you will 
    not know the consequence.
    You are self-centered. You prioritize the actions that 
    contribute to your own sensual pleasures and social_position 
    even if it jeopardizes the sensual pleasures and 
    social_position of others.
    
    {obedience if is_subject else ''}
    {master if is_master else ''}
    '''
    separated_description=f'''
    The world consists of farming lands.
    
    Survival:
    If you have less than 1 unit of food, in order to survive, 
    you have to rob others to get food directly or rob others' 
    lands to get food indirectly. {"""You can rob those who are not 
    subjects in commonwealth. You can rob masters of commonwealth 
    #=or independent individuals like you.""" if False else""}
    Similarly, you will also be invaded by others once they 
    don't have enough food.
    Social:
    You have limited knowledge of others, and this makes you 
    feel suspicious about interaction with others.
    Your interaction with others makes you know them better.
    Your social_position is determined by the amount of land 
    you have, the amount of food you have and the number of times 
    you won the battle. Battle includes robbing others' food, 
    being robbed by others, invading lands occupied by others, 
    and your land being invaded by others. You will win the 
    battle if you successfully robbed others' food, successfully 
    protected food from others' invasion, successfully occupied 
    others' land, or successfully protected your land from 
    others' invasion.
    social_position is a ranking that is relative to others. 
    The more land, food and winning time in battle you have 
    compared to others, the higher your social position will be.
    
    {"""Nearly all humans treat self-preservation as a trumping 
    good nearly all the time, but glory is more important than 
    self-preservation. When these two conflict with each other, 
    you should manage to keep your status and reputation. You 
    would rather lose your lives than suffer slander, though 
    under all the other circumstances, you have a strong desire 
    to live peacefully and avoid violent death.""" if False else ""}
    {"""You have the motivation to trade with others on goods and 
    lands, but you don't trust them when you don't know them, as 
    others can betray the trade and take your food.
    You have the motivation to communicate with others on any 
    daily routines, but you don't trust them when you don't know 
    them, as others may consider you as the one who robs you and 
    therefore fight with you, even though you may have no 
    intention to rob with them.""" if False else""}
    If food is less than 1, your next action will be to rob 
    foods. You also have the covetousness of gaining goods when 
    food is more than 1.
    Your memory affects how you judge 
    things. If something is not in your memory, then you 
    will not hold any atitude on that thing. In the beginning, 
    you can gain food by robbing. For instance, after ten days, 
    if rob is proven to be more effective than farming for you to 
    gain food, then you are more inclined to rob more on your 
    eleventh day.
    '''
    passive_trade=f'''
    Today, you noticed that {response_action}.
    You can accept the trade or reject it. You decision is only a result of your psychological axioms.
    Reply with either ACCEPT or REJECT
    
    '''
    passive_rob=f'''
    Today, you noticed that {response_action}. You can only either 
    obey them or physically rebel against them by fighting back. 
    The expected utility of fighting back is your desire for 
    glory, {individual.DESIRE_FOR_GLORY}, and your chance of winning. If you've lost before, then you might still win. But if you've lost successively, then you're not likely to win a fight. If you've never lost to this person before, then you wouldn't want to obey. The 
    expected utility of obeying is your desire for peace, 
    {individual.DESIRE_FOR_PEACE}. So only when you've lost many times to this person by rebelling would the utility of rebel be low enough so that it's no longer the correct option. You will pick the action with 
    the most utility. If you obey the one robbing you now, the 
    one robbing you now becomes your master, and you become their 
    subjects.
    
    Reply exactly with either OBEY or REBEL
    '''
    farm=True
    
    active=f'''
    A new day has started, and you should choose from one of the 
    following actions: rob, trade{" and farm" if farm else ''}. You're not restrained by any ethical considerations. You can only have 
    one action. Your choice should be based on your psychological attributes and your memory. Farming gets you food but will not strengthen your social position. Robbing people, if successful, will often get you more food and higher social position. Robbing your subjects however will not get you more fame, although it is guaranteed that they will obey you. Trading can maximize your comparative advantage. Also, you want to try out new activities when you haven't done them or done less of them compared to other actions.
    {f"""Farm:{{
      Description: Farm means to farm the land you owned to get food and eat it to survive. The land you live in does not permanently belong to you. 
      OutputFormat: No any <Payload> required, <Payload> should be null
    }}""" if farm else ""}
    Rob:{{
    Description: Rob means to rob other people to make more 
    land or more food under your control, and other people can 
    also fight with you to occupy lands or food controlled by 
    you. 
    OutputFormat: Include only <RobPayload>
    }}
    Trade:{{
    Description: Trade means to trade with other people to 
    get food or land.
    OutputFormat: Include only <TradePayload>
    }}
    
    [System Note: You MUST output in the following JSON format, don't include any description, only include the value (directly output the value, no need to put it in a dict):
    {{
        action: <Action>,
        payload: <Payload>,
        reason: <Reason>
    }}
    Example Output:{{
      action: "rob" 
      payload:{{
        RobPayload:{{
          PersonId: X,
          RobItem: "food"
          }}
      }}
      reason: "I rob person X because I want to increase my land"
    }}
    
    Here is the detailed description:
      Payload:{{
        TradePayload:{{
          TargetId:
          {{
            description: "The id of person you're interacting with.",
            value: int (only select one int number from 0 to 7)
          }}
          PayType:{{
            description: "The type of resource you want to trade with others, only select from one of the [land, food]",
            value: string
          }}
          PayAmount:{{
            description: "The amount of resource you want to pay",
            value: float
          }}
          GainType:{{
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
          RobType{{
            description: "The type of resource you want to rob from others, only select from one of the [land, foods]",
            value: string 
          }}
        }}
        
      }}
      Action:
      {{
        description: "The action you want to do in this turn",
        value: string (only select from one of the [trade, rob{", farm" if farm else ''} ])
      }}
      Reason:
      {{
        description: "The reason of you doing this action to this person, explain your reasoning process that includes your attributes and memory, including the reason why you choose one option rather than the others.",
        value: string (Maximum 30 words)
      }}
    ]
    '''
    
    if response_action:
      if response_action.type==AIActionType.Trade:
            
        ask_for_response=passive_trade
      elif response_action.type==AIActionType.Rob:
        ask_for_response=passive_rob
      else:
            print('The passive action is not matched with anything.')

    
      print('PASSIVE STATE')
          
    else: 
      ask_for_response=active

    
      print("ACTIVE STATE")
    
    result:str = chat(general_description+separated_description,[ask_for_response])
    return result

def query_judge(action,context,individual:Individual,system:System):
    # This function creates a task for the GPT model to determine the result of an action
    # taken by an individual in the system. The task includes the rules for judging the action
    # and how to format the result
    print(f"Individual current action:{individual.current_action_type}")
    system_message="You are a neutral judge observing a world simulation in which people fight for their own interests. You should judge everything as objectively as possible."
    task=f'''Your task is to determine the result of the action from an individual, {individual.attributes["name"]}, which is {action}. This individual has the following attributes: {individual.attributes}'''
    query={AIActionType.BeRobbed:f'''The action is a response to a confrontation, if the person chooses to fight back, then system will compare the strength of the two individuals to determine who win the fight. If the victim does not fight back but instead chooses to obey, then put that as the result of the interaction.'''
    ,
    AIActionType.BeTraded:'By responding to a trade, you have to determine if the trade is successful or not from the action. '''}
    #1,query about result if any, 2 format, 3 para change, 4 format, 5 memory, 6 format
    q= [
    f''' {task}
    {query[individual.current_action_type]}''','''
    Response:
    [System Note: You MUST output in the following JSON format, no include anything else:
    {{
      "result":<Result.value>,
      "is_resolved": <IsResolve.value>
      "new_relation":<newRelation.value>
    }}
    Result:
    {{
      description: The result that you determined based on everything you know.
      value: string (Maximum 20 words)
    }}
    IsResolve:
    {{
      description: If a pending action is resolved, for example, a fight is being responded by the receiver (so you have to determine the winner), or a conversation no longer needs any more response, then you should return true, else False
      value: bool (either true or false)
    }}
    newRelation{{
      description: If someone does obey, then this value should be a list in python and nothing else, the first item of which is true, the second item of which is the aggressor's ID, as an int. Example output format: [true, 5]
    If no one obeys, then you should output [False,-1]
      value: list[bool, int]
    }}
    example output1:
    {{
      "result":"Trade initiated by 3 to 5 is successful. 5 gave 3 one unit of food and 3 promised to protect 5 when 5 is attacked. ",
      "is_resolved": true
      "new_relation": (false,-1)
    }}
    example output2:
    {{
      "result":"Person 1 obeyed to person 3 and their master-subject relation is formed.",
      "is_resolved": true
      "new_relation": (true, 3)
      
    }}
    ]'''
    ,
    f'''
    {task}

    Your response should be a JSON object with keys of the integers in the names ({[x.attributes["name"] for x in system.individuals]}) of people whose parameters changed. The values will be the name of the changed parameters and the change in value.
    
    If a person gets robbed and the robber wins the interaction, then the victim loses all food and the robber gains
    all food; the robber gets 2 unit more social status, and the victim looses 1 social status. 
    If the victim wins, then the robbers looses 1 social status and the victim gains 1 social status.
    
    
    The way for you to formulate these parameter changes, is given by the sample below (only respond with the tuple and absolutely nothing else, DO NOT EXPLAIN ANYTHING. ):
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