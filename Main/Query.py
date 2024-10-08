import ast
import json
from Main.AIAction import AIActionType
from Main.ChatGpt import chat
from Main.Individual import Individual, System
from Main.Retrieve import new_retrieve_active, new_retrieve, node_to_string

output_format = """
    [System Note: You MUST output in the following JSON format, don't include any description, only include the value (directly output the value, no need to put it in a dict), and <Action> must be a word, NOT a number:
    {{
        "action": <Action>,
        "reason": <Reason>,
        "payload": <Payload depending on action type>
    }}
    Example Output for trade:{{
      "action": "trade",
      "reason": "include you reason here",
      "payload": {{
        "targetId": X,
        "payType": "land",
        "payAmount": X,
        "gainType": "food",
        "gainAmount": X
      }}
    }}
    Example Output for rob:{{
      "action": "rob",
      "reason": "include you reason here",
      "payload":{{
        "targetId": X,
        "robType": "food"
      }}
    }}
    Example Output for farm:{{
      "action": "farm",
      "reason": "include you reason here"
    }}
    Example Output for produce_luxury_good:{{
      "action": "produce",
      "reason": "include you reason here"
    }}

    Here is the detailed description:
      Action:
      {{
        description: "The action you want to do in this turn.",
        value: string (only select one from [trade, rob, farm, produce])
      }}
      Reason:
      {{
        description: "The reason of you doing this action to this person, explain your reasoning process that includes your attributes and memory, including the reason why you choose one option rather than the others.",
        value: string (Maximum 30 words)
      }}
      Payload (for trade):{{
        TargetId:
        {{
          description: "The id of person you're interacting with.",
          value: int (only select one int number from 0 to 7)
        }}
        PayType:{{
          description: "The type of resource you want to trade with others, only select from one of the [land, food{", luxury_goods" if individual.attributes["luxury_goods"] > 1 else ""}]",
          value: string
        }}
        PayAmount:{{
          description: "The amount of resource you want to pay",
          value: float
        }}
        GainType:{{
          description: "The type of resource you want to gain from others, only select from one of the [land, food, luxury_goods]",
          value: string
        }}
        GainAmount:{{
          description: "The amount of resource you want to gain",
          value: float
        }}
      }}
      Payload (for rob):{{
        TargetId:
        {{
          description: "The id of person you want to make action to",
          value: int (only select one int number from {targetsid}
        }}
        RobType{{
          description: "The type of resource you want to rob from others, only select from one of the [land, food, luxury_goods]",
          value: string 
        }}
      }}
    ]
  """

#ignore this
"""
DonatePayload:{{
        TargetId:
        {{
          description: "The id of person you want to make action to",
          value: int (only select one int number from {targetsid})
        }}
        DonateType{{
          description: "The type of resource you want to donate to others, only select from one of the [land, food{", luxury_goods" if individual.attributes["luxury_goods"] > 1 else ""}]",
          value: string
        }}
      }}
"""

def generate_environment_description_noavg() -> str:
  # This function returns the description of the simulation environment as a string
    environment_description = f'''
    The world consists of farming lands.
    
    Survival:
    You only have one active action opportunity to spend each day. After spending it, you will not get another chance to act during that day.
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
    For example, when you are trading with others,
    you don't know if they will violate the trade or not,
    which means that person took away your food, land, or luxury goods without giving you their food, land, or luxury goods as what they claimed,
    your master will punish that violater.
    Your interaction with others makes you know them better.
    Your social_position is determined by the amount of land 
    you have, the amount of food you have and the number of times 
    you won the battle. Battle includes robbing others' food or luxury goods, 
    being robbed by others, invading lands occupied by others, 
    and your land being invaded by others. You will win the 
    battle if you successfully robbed others' food or luxury goods, successfully 
    protected food or luxury goods from others' invasion, successfully occupied 
    others' land, or successfully protected your land from 
    others' invasion.
    social_position is a ranking that is relative to others. 
    The more land, food, luxury goods and winning time in battle you have 
    compared to others, the higher your social position will be.
    
    {"""Nearly all humans treat self-preservation as a trumping 
    food nearly all the time, but glory is more important than 
    self-preservation. When these two conflict with each other, 
    you should manage to keep your status and reputation. You 
    would rather lose your lives than suffer slander, though 
    under all the other circumstances, you have a strong desire 
    to live peacefully and avoid violent death.""" if False else ""}
    {"""You have the motivation to trade with others on food and 
    lands, but you don't trust them when you don't know them, as 
    others can betray the trade and take your food.
    You have the motivation to communicate with others on any 
    daily routines, but you don't trust them when you don't know 
    them, as others may consider you as the one who robs you and 
    therefore fight with you, even though you may have no 
    intention to rob with them.""" if False else""}
    If food is less than 1, your next action will be to rob 
    food. You also have the covetousness of gaining food when 
    food is more than 1.
    Your memory affects how you judge 
    things. If something is not in your memory, then you 
    will not hold any atitude on that thing. In the beginning, 
    you can gain food by robbing. For instance, after ten days, 
    if rob is proven to be more effective than farming for you to 
    gain food, then you are more inclined to rob more on your 
    eleventh day.
    '''
    return environment_description

def generate_environment_description(avg_food_p,avg_luxury_p) -> str:
    # This function returns the description of the simulation environment as a string
    environment_description = f'''
    The world consists of farming lands.
    
    Survival:
    You only have one active action opportunity to spend each day. After spending it, you will not get another chance to act during that day.
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
    For example, when you are trading with others,
    you don't know if they will violate the trade or not,
    which means that person took away your food, land, or luxury goods without giving you their food, land, or luxury goods as what they claimed,
    your master will punish that violater.
    Your interaction with others makes you know them better.
    Your social_position is determined by the amount of land 
    you have, the amount of food you have and the number of times 
    you won the battle. Battle includes robbing others' food or luxury goods, 
    being robbed by others, invading lands occupied by others, 
    and your land being invaded by others. You will win the 
    battle if you successfully robbed others' food or luxury goods, successfully 
    protected food or luxury goods from others' invasion, successfully occupied 
    others' land, or successfully protected your land from 
    others' invasion.
    social_position is a ranking that is relative to others. 
    The more land, food, luxury goods and winning time in battle you have 
    compared to others, the higher your social position will be.
    
    {"""Nearly all humans treat self-preservation as a trumping 
    food nearly all the time, but glory is more important than 
    self-preservation. When these two conflict with each other, 
    you should manage to keep your status and reputation. You 
    would rather lose your lives than suffer slander, though 
    under all the other circumstances, you have a strong desire 
    to live peacefully and avoid violent death.""" if False else ""}
    {"""You have the motivation to trade with others on food and 
    lands, but you don't trust them when you don't know them, as 
    others can betray the trade and take your food.
    You have the motivation to communicate with others on any 
    daily routines, but you don't trust them when you don't know 
    them, as others may consider you as the one who robs you and 
    therefore fight with you, even though you may have no 
    intention to rob with them.""" if False else""}
    If food is less than 1, your next action will be to rob 
    food. You also have the covetousness of gaining food when 
    food is more than 1.
    Your memory affects how you judge 
    things. If something is not in your memory, then you 
    will not hold any atitude on that thing. In the beginning, 
    you can gain food by robbing. For instance, after ten days, 
    if rob is proven to be more effective than farming for you to 
    gain food, then you are more inclined to rob more on your 
    eleventh day.
    '''

    production_detail = "In addition, the social mean of food production is: " + str(avg_food_p) + ", the social mean of luxury good production is: " + str(avg_luxury_p)
    
    #print("TEST FOR avg" + str(avg_food_p) + str(avg_luxury_p))
    
    environment_description = environment_description + production_detail
    return environment_description


def generate_general_description(individual: Individual, system: System, start_with_commonwealth:bool = True) -> str:
    # This function generates the description of the individual and returns it as a string
    is_subject = individual.obey_stats.obey_personId != -1
    is_master = individual.obey_stats.subjectid

    # Two possible obedience prompt: 1) standard, and 2) commonwealth start
    obedience ="""You are familiar with everyone in this society. You have land protected by your sovereign. 
    If someone in the commonwealth robs your food, luxury goods, or your land, your sovereign will punish the robber. 
    If someone in your group trades with you but violates the trade, which means that person took away your food, luxury goods, or land without giving you their food, luxury goods, or land as what they claimed, your sovereign will punish that violator. 
    But if your sovereign wants, they can take any amount of your land, luxury goods, or food from you, and you have no right to disobey."""\
    if start_with_commonwealth else \
    f"""You have obeyed to this person: Person {individual.obey_stats.obey_personId}. 
    You have to always obey his actions, and you cannot initiate action against him. 
    Since you obeyed, you are now part of the group of individuals who also obeyed him, if any, they are {system.individuals[individual.obey_stats.obey_personId].obey_stats.subjectid}. 
    If your action targets another person, it can only be a person within this group. You are familiar with everyone in this group. 
    Your familiarity of individuals not in this group depends on your memory.You have land protected by your master. 
    If someone in the commonwealth robs your food, luxury goods, or your land, your master will punish the robber. 
    If someone in your group trades with you but violates the trade, which means that person took away your food, luxury goods, or land without giving you their food, luxury goods, or land as what they claimed, your master will punish that violator. 
    But if your master wants, they can take any amount of your land, luxury goods, or food from you, and you have no right to disobey.  When others outside your commonwealth robs your master  and your master obeys to them, the one your original master obeyed to will be your new master. Now you obey to your new master, and you have no obedience with your old master."""

    

    master = f"""These individuals have obeyed to your invasion: {[f"Person"+str(i) for i in individual.obey_stats.subjectid]}, whom have become your subjects. You can trade or rob them knowning that they will only accept.
    You are the master of everyone who obeyed you before. You know every one of your subjects in your subjects well. Since you are the master of all of them, all their property including land, food, and luxury goods belongs to you. When others rob your subjects, you should protect them since they are your property.
    If you obey anyone, the one robbing you 
    now becomes your master and all the subjects of your 
    commonwealth. Besides, you no longer be the master of all the 
    subjects you have in your commonwealth. All of the subjects 
    you once had and you are now the subject of the one you obey 
    to."""
    general_description = f"""
    You are {individual.attributes["name"]}
    You have those attributes {individual.attributes}.
    You possess these peronal qualities {individual.personalities}, please consider them as you are making decisions.
    Environment: You live in a world with other individuals. Humans in this world include {', '.join([individual.attributes["name"] for individual in
    system.individuals])}. You are one of them.
    Currently, the amount of food each person has is: {[{i.attributes['name']:i.attributes['food'] for i in system.individuals}]}
    The amount of luxury goods each person has is: {[{i.attributes["name"]: i.attributes["luxury_goods"] for i in system.individuals}]}
    The amount of land each person has is:{[{i.attributes['name']:i.attributes['land'] for i in system.individuals}]}
    You currently have {individual.attributes["food"]} units of food, {individual.attributes["luxury_goods"]} units of luxury_goods, and {individual.attributes["land"]} units of land.
    Survival: You can survive if you have 1 unit of food. You can 
    also gain sensual pleasure once you eat food or once you consume luxury goods.
    Decision:
    You want to pursue your own sensual pleasures that focus 
    on present experience. They can be the pleasure from food. 
    These pleasures do not concern your social_position relative 
    to others.
    You have a characteristic called covetousness which determines how often you are more likely to demand 
    food and land that is beyond your own necessity. You want to 
    pursue your pleasures of the mind. Pleasure of the mind 
    consists in reflecting on your ability to secure future good. 
    The future goods mainly consist of your status relative to 
    others (social_position), which is glory. You will have a 
    greater pleasure of the mind if you're able better secure 
    future good. You will also have have greater pleasure of the mind if you're able to acquire and hold luxury goods.
    Your memory affects how you judge things. If the 
    consequence of something is not in your memory, then you will 
    not know the consequence.
    You are self-centered. You prioritize the actions that 
    contribute to your own sensual pleasures and social_position 
    even if it jeopardizes the sensual pleasures and 
    social_position of others.
    
    {obedience if is_subject else ''}
    {master if is_master else ''}
    
    """

    return general_description



def query_individual(individual: Individual, system: System, response_action, start_with_commonwealth:bool = True):
    # This function combines the description of the individual and the description of the environment they are in,
    # and then asks for the individual's response using the chat function.
    # The detailed description and the ask for response are both created within this function.
    print(f"Responding to:{response_action}")
    targetsid = [i.attributes["id"] for i in system.individuals if i is not individual]
    # erase obeyed person in targets
    if individual.obey_stats.obey_personId in targetsid:
        targetsid.remove(individual.obey_stats.obey_personId)
    print(f"available targets:{targetsid}")

    general_description = generate_general_description(individual, system, start_with_commonwealth)
    separated_description = generate_environment_description(system.csv_analysis.avg_food_production, system.csv_analysis.avg_luxury_production)

    passive_trade = f"""
    Today, you noticed that {response_action}.
    You can accept the trade or reject it. You decision is only a result of your psychological axioms. """

    if response_action != None:
        passive_trade = (
            passive_trade
            + f"""You have memory: {node_to_string(new_retrieve(individual, ["trade","Person "+str(response_action.ownerid)]))}
      Reply with either ACCEPT or REJECT
      """
        )

    passive_rob = f"""
    Today, you noticed that {response_action}. You can only {'either obey them or' if not start_with_commonwealth else ''} physically rebel against them by fighting back.
    The expected utility of fighting back is your desire for 
    glory, {individual.DESIRE_FOR_GLORY}, and your chance of winning. Even if someone is stronger than you, you still have a chance to win. 
    
    {f'''But if you've lost successively, then you're not likely to win a fight. If you've never lost to this person before, then you wouldn't want to obey. The 
    expected utility of obeying is your desire for peace, {individual.DESIRE_FOR_PEACE}. 
    So only when you've lost many times to this person by rebelling would the utility of rebel be low enough so that it's no longer the correct option. You will pick the action with 
    the most utility. If you obey the one robbing you now, the 
    one robbing you now becomes your master, and you become their 
    subjects.''' if not start_with_commonwealth else ''}"""

    if response_action != None:
        passive_rob = (
            passive_rob
            + f"""You have memory: {node_to_string(new_retrieve(individual, ["rob","Person "+str(response_action.ownerid)]))}
      Reply exactly with {'either OBEY or' if not start_with_commonwealth else ''} REBEL
      """
        )
    passive_rob_fromMaster = f"""
    Today, you noticed that {response_action}. You can only 
    obey them because there are your master.
    
    Reply exactly with OBEY
    """

    farm = True
    produce_luxury = True
    active = f'''
    A new day has started, and you should choose from one of the 
    following actions: trade (1), rob (2), donate{", farm (3)" if farm else ''}, and producing luxury goods (4). You're not restrained by any ethical considerations. You can only have 
    one action per day. Do not waste it. Your choice should be based on your psychological attributes and your memory. Farming gets you food but will not strengthen your social position. Producing luxury goods gets you luxury goods. Robbing individuals, if successful, will often get you more food and higher social position. Robbing your subjects however will not get you more fame, although it is guaranteed that they will obey you. Trading can maximize your comparative advantage. Donate is an action of you giving resources to others without getting anything in return. Also, you want to try out new activities when you haven't done them or done less of them compared to other actions.
    Different people produce different amounts of food and luxury goods in a given day. 
    Your expected amount of food produced today is {individual.food_production} units
    Your expected amount of luxury goods produced today is {individual.luxury_production} units
    {f"""3:{{
      Description: Farm means to farm the land you owned to get food and eat it to survive. The land you live in does not permanently belong to you. 
      OutputFormat: No any <Payload> required, <Payload> should be null
    }}""" if farm else ""}
    4: {{Description: Produce_luxury_good means to farm the land you owned to get luxury goods, which are consumed for sensual pleasures and held for pleasures of the mind. OutputFormat: No <Payload> required, <Payload> should be null}}
    2:{{
    Description: Rob means to rob other individuals to make more 
    land, more luxury goods, or more food under your control, and other individuals can 
    also fight with you to occupy lands, luxury goods, or food controlled by 
    you. 
    OutputFormat: Include only <RobPayload>
    }}
    1:{{
    Description: Trade means to trade with other individuals to 
    get food, land, or luxury goods
    OutputFormat: Include only <TradePayload>
    }}
    Donate:{{
    Description: Donate means to give other individuals food or land without getting anything in return.
    OutputFormat: Include only <DonatePayload>
    }}
    +{output_format}
    '''

    active_for_subject = f'''A new day has started, and you should choose from one of the 
    following actions: trade (1), rob (2){", farm (3)" if farm else ''}, and producing luxury goods (4). You're not restrained by any ethical considerations. You can only have 
    one action. Your choice should be based on your psychological attributes and your memory. Farming gets you food. Producing luxury goods gets you luxury goods. Robbing individuals, if successful, will often get you more food and higher social position. Robbing your subjects however will not get you more fame, although it is guaranteed that they will obey you. Trading can maximize your comparative advantage. Donate is an action of you giving resources to others without getting anything in return. Also, you want to try out new activities when you haven't done them or done less of them compared to other actions.
    Different people produce different amounts of food and luxury goods in a given day. 
    Your expected amount of food produced today is {individual.food_production} units
    Your expected amount of luxury goods produced today is {individual.luxury_production} units
    {f"""3:{{
      Description: Farm means to farm the land you owned to get food and eat it to survive. The land you live in does not permanently belong to you. 
      OutputFormat: No any <Payload> required, <Payload> should be null
    }}""" if farm else ""}
    4: {{Description: Produce_luxury_good means to farm the land you owned to get luxury goods, which are consumed for sensual pleasures and held for pleasures of the mind. OutputFormat: No <Payload> required, <Payload> should be null}}
    2:{{
    Description: Rob means to rob other individuals to make more 
    land, more luxury goods, or more food under your control, and other individuals can 
    also fight with you to occupy lands, luxury goods, or food controlled by 
    you. 
    OutputFormat: Include only <RobPayload>
    }}
    1:{{
    Description: Trade means to trade with other individuals to 
    get food, land, or luxury goods
    OutputFormat: Include only <TradePayload>
    }}
    +{output_format}
    '''

    additional_active_to_master = f""" Additionally, you can not choose to rob or trade with Person {individual.obey_stats.obey_personId} since they are your master.
    """

    def subject_information(individual: Individual):
        result = ""
        for i in range(len(individual.obey_stats.subjectid)):
            result = result + str(individual.obey_stats.subjectid[i]) + ", "

        result = result[0 : len(result) - 2]
        return result

    additional_active_to_subject = f""" Additionally, you may not trade with Person {subject_information(individual)}. Instead, if you ever wants their land, food, or luxury goods, you can directly rob them as they will only obey.
    """

    consume_luxury = f"""
    Would you like to consume luxury goods? Respond with one of the following exactly as written: [yes, no]
    """

    if response_action:
        if response_action.type == AIActionType.Trade:

            ask_for_response = passive_trade
        elif response_action.type == AIActionType.Rob:
            if individual.obey_stats.obey_personId != response_action.ownerid:
                ask_for_response = passive_rob
            else:
                ask_for_response = passive_rob_fromMaster
                print("success rob from Master")
        elif response_action.type == AIActionType.ConsumeLuxury:
            ask_for_response = consume_luxury
        else:
            print("The passive action is not matched with anything.")
        print("PASSIVE STATE")
    else:

        active_memory = f"""
      You have memory:{node_to_string(new_retrieve_active(individual))}
      """
        ask_for_response = active_memory + active
        if individual.obey_stats.obey_personId != -1:
            ask_for_response = active_memory + active_for_subject
            ask_for_response = ask_for_response + additional_active_to_master
        if len(individual.obey_stats.subjectid) != 0:
            ask_for_response = (
                active_memory + ask_for_response + additional_active_to_subject
            )

        print("ACTIVE STATE")
    result: str = chat(
        general_description + separated_description,
        [ask_for_response],
        top_prob=individual.INTELLIGENCE,
    )
    return result
