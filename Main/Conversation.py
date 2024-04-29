import json
from openai import OpenAI
from autogen import GroupChatManager
from typing import List, Dict
from Main.Individual import Individual
from Main.System import System
from Main.Memory import ConceptNode
from Main.SpeakingAgent import SpeakingAgent, CustomGroupChat
from Main.Query import generate_environment_description_noavg, generate_general_description
from Main.Retrieve import new_retrieve
from Main.ChatGpt import AUTOGEN_LLM_CONFIG 

client = OpenAI(api_key=AUTOGEN_LLM_CONFIG["config_list"][0]["api_key"])

def converse(individuals: List[Individual], system: System, chat_topic: str, pleasure_system_input: str = None) -> List[Dict[str, str]]:
    '''
    initiate a conversation between individuals with AutoGen GroupChat
    returns the conversation content as a json object

    chat_topic: a string describing the topic of discussion for this groupchat. It will be used to retrieve relevant memories

    '''

    speak_for_yourself_msg = "DO NOT GENERATE RESPONSES FOR OTHER AGENTS, ONLY SPEAK FOR YOURSELF."

    terminate_chat_when_agreed_msg = "When EVERYONE in the conversation has CLEARLY formed an agreement on a topic, reply the word 'TERMINATE' by itself"

    consider_traits_msg = "You should really consider how your personality traits and memory influences you before you respond."

    self_centered_msg = "you are self-centered, so you're making policies that best satisfy your own interests. Your citizens' interests are your interests"

    consider_resources_msg = "IMPORTANT: you also want to have a better social position than others, meaning you want to have more resources than others, more food, \
                            luxury good, and land. If your current resources are less than other people's, you would feel uncontent and try to increase your resources. \
                            Otherwise, if you have more resources than others, you would be content and try to maintain that advantage."

    system_msg = f"""[System Note: {speak_for_yourself_msg}\n{terminate_chat_when_agreed_msg}\n{consider_traits_msg}\n{self_centered_msg}\n{consider_resources_msg}]\n"""

    # udpate the system message of each agent with game rules/ setting, retrieved memory, personality, pleasure system output (not implemented), and personal status (not implemented)
    for i, person in enumerate(individuals, 0):

        environment_description = generate_environment_description_noavg()

        general_description = generate_general_description(person, system)

        # retrieves relevant memories 
        retrieved_memories = new_retrieve(person, [chat_topic], 10)
        # iterate through all relavant memories and concatenate as one string
        relevant_memory_descriptions = "Relevant memories:\n" + "\n".join([node.description for node in retrieved_memories])

        personality_string = "\n".join(person.get_personality())

        # update the agent with the new system prompt
        new_msg = "\n".join([environment_description, general_description, relevant_memory_descriptions, system_msg])
        person.update_agent_prompt(new_msg)
        # update its speaking tendency
        tendency = evaluate_speaking_tendencies(personality_string)
        person.update_agent_speaking_tendency(tendency)


    # create a groupchat
    agents = [person.get_agent() for person in individuals]
    groupchat = CustomGroupChat(agents=agents, messages=[], max_round=100)
    manager = GroupChatManager(groupchat=groupchat, llm_config=AUTOGEN_LLM_CONFIG, human_input_mode="NEVER")

    # create a agent for system message exclusively
    system_agent = SpeakingAgent(name="system", system_message="", llm_config=AUTOGEN_LLM_CONFIG)

    example_responses = [
        # "response 1: I have mixed feelings about the policy. While I understand the potential benefits of offering a subsidy for luxury goods production, I am somewhat cautious about its impact on overall societal well-being. I believe it is important to consider the allocation of resources and ensure that basic needs, such as food, are adequately met before prioritizing luxury goods.",
        # "response 2: I am generally organized and prefer routine. I believe that offering a 20 percent subsidy to luxury goods producers could potentially disrupt the balance of our society. It may lead to an overemphasis on luxury goods production, which could divert resources and attention away from essential needs like food production. We should prioritize maintaining a balanced economy and ensuring the availability of essential goods for all.",
        # "response 3: I am self-centered. Since I more food than most of the other people, I don't support the redistibution of resources as my food would be taken from me and given to other people. This is bad because it lowers my chances of survival.",
        # "response 4: Since I only have 1 unit of food left but have 30 units of luxury goods, I support the idea of increased trading, as that will allow me to trade off some of my luxury good and quickly gain food so that I won't starve.",
        "Example response 1: I'm quite satisfied with my life. As someone who mainly produces food from my land of 10 units, I'm self-sufficient. I also trade my food with others in exchange for luxury good. Consuming them brings me a lot of pleasures.",
        "Example response 2: I felt my life sucked. I have only 2 unit of land and produce food from there. I often felt starved. I can hardly sustain myself. I need more food to survive. If possible I also wish to get some luxury good for my pleasure.",
        "Example response 3: I have a mixed feeling about my life. I have a lot of food and land so I don't have to worry about my survival too much. But I have a poor ability to produce luxury good. I have to trade luxury goods from others with my food, which is quite costly. I hope the trade would be more fairer.",
        "Example response 4: I'm not quite happy with the society. Although I have 100 units of food and 50 units of luxury good, Someone else in our society has 500 units of food and 300 units of luxury good. That's not fair. I want to have more resources as well."
    ]

    example_responses_str = '\n'.join(example_responses)

    initial_msg = f"""
    System Message: Now, several members of the society have gathered to discuss their opinion about the world that they live in.
    The topic is: {chat_topic}
    You are allowed to debate with other people for your opinions.
    DO NOT use modern terms that are too abstract for the world setting.
    Limit each response to 50 words.

    Here are several examples of how your should structure your responses:
    {example_responses_str}
    """

    # initiate conversation. silent=False for testing/debugging
    system_agent.initiate_chat(manager, message=initial_msg, silent=False)

    # returns the messages as a json object
    messages = groupchat.messages

    return messages



def add_memory_after_conversation(individuals: Individual, conversation: List[Dict[str, str]]) -> None:
    '''
    summarizes the contents of the conversation and adds a new memory from the perspective of each participant of the conversation
    '''

    individuals_ids = [person.attributes["id"] for person in individuals]

    for person in individuals:
        # system message instructing gpt to summarize the conversation
        content = f'''
        Please read the following conversation, and summarize the contents pretending to be {person.attributes['name']}, from a first person perspective.
        Talk about your specific actions, and focus more on yourself. 
        Limit the summary to 50 words'''

        system_msg = {"role": "system", "content": content}
        # generate description; exclude the first and last message
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[system_msg] + conversation[1:-1],top_p=person.INTELLIGENCE)
        memory_description = response.choices[0].message.content

        # create a new concept node
        # ID will just be current number of concept nodes stored + 1
        node = ConceptNode(person.memorystream.get_memory_length() + 1, "chat", -1, person.attributes["id"], "chat with", individuals_ids, -1, memory_description, -1)
        person.memorystream.add_concept_node(node)

def evaluate_speaking_tendencies(personality_description: str) -> str:
    '''
    Given the personality (big 5) of an individual, ask gpt to return "FREQUENT", "SOMETIMES", or "SELDOM"
    as their speaking tendency
    '''

    msg = {"role": "system", "content": personality_description}

    task_description = '''
    Please read the above description of someone's personality traits.
    Then, choose one of the three words below that best describe how often this person would speak during a group conversation:

    FREQUENT: This person speaks very often throughout the entire conversation.
    SOMETIMES: This person speaks occasionally at times throughout the conversation.
    SELDOM: This person rarely speaks out during a group conversation.

    Only return the word in all captial letters. No description is needed.
    '''

    system_msg = {"role": "system", "content": task_description}

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[msg, system_msg], temperature=0.0)
    speaking_tendency = response.choices[0].message.content

    return speaking_tendency


def summarize_conversation(conversations: List[List[Dict[str, str]]]) -> str:
    '''
    Given multiple conversations, ask gpt to summarize and categorize the contents by agent's sentiment (content, somewhat content, and not content)
    and list who those people are, for want reason, and any suggested policy.
    '''

    messages = []

    for i, convo in enumerate(conversations, 1):
        messages.append({"role": "system", "content": f"This is the start of conversation number {i}"})
        messages.extend(convo)

    task_description_categorize = '''
    Please read the above conversations of people in a society disscussing their opinions about the world they live in.
    First, based on how their opinions about the world, categorize the people into one of the following category:
    1. Content
    2. Somewhat Content
    3. Not Content

    IMPORTANT: all individuals in the conversation must be included in exactly one category
    if an category is empty, indicate it as "None".

    Here is an example output:
    Content: person_1, person_3, person_5
    Somewhat Content: None
    Not Content: person_2, person_4

    '''
    task_description_summarize = '''

    Next, for each category, summarize the contents of their conversations into the format below. It MUST be strictly in this format:

    Sentiment: <The category: "Content", "Somewhat Content", or "Not Content">
        Individuals: <the people who are in this category>
        Reasons: <A list of reasons why those listed individuals feel this way. Only information presented in the conversation should be used to create these reasons, and these reasons should only be from the individuals that were listed above>
        Suggested Changes: <A list of changes, if any, suggested by the individuals listed above. If they did not mention any changes, put "None">

    If there are several reasons that are similar, combine them into one. 

    Here is an example summary of the 3 categories:


    Sentiment: Not Content
        Individuals: person_2, person_5
        Reasons: both person_2 and person_5 currently have 0 units of food, and they often feel starved. 
        Suggested Changes: increase the amount of food they receive from trading by 10 percent.

    Sentiment: Content
        Individuals: person_1
        Reasons: person_1 has 40 units of food and is able to sustain themselves.
        Suggested Changes: None
    
    Sentiment: Somewhat Content
        Individuals: person_3, person_4
        Reasons: person_3 has 20 units of food and is able to sustain themselves, but keeps getting robbed by other people. person_4 has enough food, but 0 units of luxury good.
        Suggested Changes: None
    
    
    Output the summaries strictly according to the given format
    IMPORTANT: There may only be at most one summary for each category.
    '''

    categorization_msg = {"role": "system", "content": task_description_categorize}
    messages.append(categorization_msg)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, temperature=0.0)
    categories = response.choices[0].message.content

    system_msg = {"role": "system", "content": f"Here are the categories:\n{categories}"}
    messages.append(system_msg)
    summarization_msg = {"role": "system", "content": task_description_summarize}
    messages.append(summarization_msg)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, temperature=0.0)
    summaries = response.choices[0].message.content

    return summaries





