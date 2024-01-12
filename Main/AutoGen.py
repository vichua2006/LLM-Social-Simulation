import json
from typing import List, Optional
from autogen import AssistantAgent, GroupChat, GroupChatManager
from Main.Individual import Individual
from Main.Query import generate_environment_description, generate_general_description
from Main.System import System
from Main.Retrieve import new_retrieve

from Main.Individual import AGENT_LLM_CONFIG # there has to be a better way to do this



def converse(individuals: List[Individual], system: System, chat_topic: str, temp_personalities: List[str], pleasure_system_input: str = None) -> str:
    '''
    initiate a conversation between individuals with AutoGen GroupChat
    returns the conversation content as a json string

    chat_topic: a string describing the topic of discussion for this groupchat. It will be used to retrieve relevant memories

    temp_personalities is a temporary variable to pass in the personality descriptions (big 5) of each individual; not sure how it should be done
    '''

    speak_for_yourself_msg = """DO NOT GENERATE RESPONSES FOR OTHER AGENTS, ONLY SPEAK FOR YOURSELF."""

    terminate_chat_when_agreed_msg = """When everyone in the conversation has formed an agreement on a topic, reply "TERMINATE" """

    system_msg = f"""
    [System Note: 
    {speak_for_yourself_msg} 
    {terminate_chat_when_agreed_msg}
    ]
    """

    # udpate the system message of each agent with game rules/ setting, retrieved memory, personality (incomplete), pleasure system output (not implemented), and personal status (not implemented)
    for i, person in enumerate(individuals, 0):

        environment_description = generate_environment_description()
        general_description = generate_general_description(person, system)

        # retrieves relevant memories 
        retrieved_memories = new_retrieve(person, [chat_topic], 1)
        # iterate through all relavant memories and concatenate as one string
        relevant_memory_descriptions = "\n".join([node.description for node in retrieved_memories[chat_topic]])

        personality = temp_personalities[i]

        new_msg = "\n".join([environment_description, general_description, relevant_memory_descriptions, personality, system_msg])
        person.update_agent_prompt(new_msg)
    


    # create a groupchat
    agents = [person.get_agent() for person in individuals]
    groupchat = GroupChat(agents=agents, messages=[], max_round=100)
    manager = GroupChatManager(groupchat=groupchat, llm_config=AGENT_LLM_CONFIG)

    initial_msg = f"""
    System Message: Now, several members of the society have gathered to discuss their opinion about the society that they live in.
    The policy is: {chat_topic}.
    You MUST speak and reply based on your personality and memories. Limit each response to 50 words.
    """

    # initiate conversation. silent=False for testing/debugging
    agents[0].initiate_chat(manager, message=initial_msg, silent=False)










