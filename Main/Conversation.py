import json
from openai import OpenAI
from typing import List, Dict
from autogen import GroupChatManager
from Main.Individual import Individual
from Main.System import System
from Main.Memory import ConceptNode
from Main.SpeakingAgent import SpeakingAgent, CustomGroupChat
from Main.Query import generate_environment_description, generate_general_description
from Main.Retrieve import new_retrieve

from Main.config import AUTOGEN_LLM_CONFIG 
client = OpenAI(api_key=AUTOGEN_LLM_CONFIG["config_list"][0]["api_key"])

def converse(individuals: List[Individual], system: System, chat_topic: str, personalities: List[str], pleasure_system_input: str = None) -> List[Dict[str, str]]:
    '''
    initiate a conversation between individuals with AutoGen GroupChat
    returns the conversation content as a json object

    chat_topic: a string describing the topic of discussion for this groupchat. It will be used to retrieve relevant memories

    personalities is a temporary variable to pass in the personality descriptions (big 5) of each individual; not sure how it should be done
    '''

    speak_for_yourself_msg = """DO NOT GENERATE RESPONSES FOR OTHER AGENTS, ONLY SPEAK FOR YOURSELF."""

    terminate_chat_when_agreed_msg = """When EVERYONE in the conversation has CLEARLY formed an agreement on a topic, reply the word "TERMINATE" by itself"""

    system_msg = f"""
    [System Note: 
    {speak_for_yourself_msg} 
    {terminate_chat_when_agreed_msg if True else ""}
    ]
    """

    # udpate the system message of each agent with game rules/ setting, retrieved memory, personality, pleasure system output (not implemented), and personal status (not implemented)
    for i, person in enumerate(individuals, 0):

        environment_description = generate_environment_description()
        general_description = generate_general_description(person, system)

        # retrieves relevant memories 
        retrieved_memories = new_retrieve(person, [chat_topic], 1)
        # iterate through all relavant memories and concatenate as one string
        relevant_memory_descriptions = "Here are some relevant memories that you have:\n" + "\n".join([node.description for node in retrieved_memories])

        personality_description = f'''
        Here are some descriptions about your personality. You must talk and behave according to these descriptions.
        {personalities[i]}
        '''

        # update the agent with the new system prompt
        new_msg = "\n".join([environment_description, general_description, personality_description, relevant_memory_descriptions, system_msg])
        person.update_agent_prompt(new_msg)
        # update its speaking tendency
        tendency = evaluate_speaking_tendencies(personalities[i])
        person.update_agent_speaking_tendency(tendency)

        # testing
        print(tendency)
    


    # create a groupchat
    agents = [person.get_agent() for person in individuals]
    groupchat = CustomGroupChat(agents=agents, messages=[], max_round=100)
    manager = GroupChatManager(groupchat=groupchat, llm_config=AUTOGEN_LLM_CONFIG)

    # create a agent for system message exclusively
    system_agent = SpeakingAgent(name="system", system_message="", llm_config=AUTOGEN_LLM_CONFIG)


    initial_msg = f"""
    System Message: Now, several members of the society have gathered to discuss their opinion about the world that they live in.
    The topic is: {chat_topic}.
    You are allowed to debate with other people for your opinions
    Limit each response to 50 words.
    """

    # initiate conversation. silent=False for testing/debugging
    system_agent.initiate_chat(manager, message=initial_msg, silent=False)

    # returns the messages as a json object
    messages = groupchat.messages

    # debugging
    print(json.dumps(messages, indent=4))

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







