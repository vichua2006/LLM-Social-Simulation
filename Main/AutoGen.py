import json
from openai import OpenAI
from typing import List, Optional, Dict
from autogen import AssistantAgent, GroupChat, GroupChatManager
from Main.Individual import Individual
from Main.System import System
from Main.Memory import ConceptNode
from Main.Query import generate_environment_description, generate_general_description
from Main.Retrieve import new_retrieve

from Main.Individual import AGENT_LLM_CONFIG # there has to be a better way to do this
client = OpenAI(api_key=AGENT_LLM_CONFIG["config_list"][0]["api_key"])


def converse(individuals: List[Individual], system: System, chat_topic: str, temp_personalities: List[str], pleasure_system_input: str = None) -> List[Dict[str, str]]:
    '''
    initiate a conversation between individuals with AutoGen GroupChat
    returns the conversation content as a json object

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
        relevant_memory_descriptions = "Here are some relevant memories that you have:\n" + "\n".join([node.description for node in retrieved_memories[chat_topic]])

        personality = temp_personalities[i]

        new_msg = "\n".join([environment_description, general_description, relevant_memory_descriptions, personality, system_msg])
        person.update_agent_prompt(new_msg)
    


    # create a groupchat
    agents = [person.get_agent() for person in individuals]
    groupchat = GroupChat(agents=agents, messages=[], max_round=100)
    manager = GroupChatManager(groupchat=groupchat, llm_config=AGENT_LLM_CONFIG)

    initial_msg = f"""
    System Message: Now, several members of the society have gathered to discuss their opinion about the society that they live in.
    The topic is: {chat_topic}.
    You MUST speak and reply based on your personality and memories. Limit each response to 50 words.
    """

    # initiate conversation. silent=False for testing/debugging
    agents[0].initiate_chat(manager, message=initial_msg, silent=False)

    # returns the messages as a json object
    messages = groupchat.messages

    # debugging
    print(json.dumps(messages, indent=4))

    return messages



def add_memory_after_conversation(individuals: Individual, conversation: List[Dict[str, str]]) -> None:
    '''
    summarizes the contents of the conversation and adds a new memory from the perspective of each participant of the conversation

    Is there a more efficient way to do this?
    '''

    individuals_ids = [person.attributes["id"] for person in individuals]

    for person in individuals:
        # system message instructing gpt to summarize the conversation
        system_msg = {"role": "system", "content": f"Please read the following conversation, and summarize the contents from the perspective of {person.attributes['name']}. Ignore the contents of the first and very last message"}
        # generate description 
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[system_msg] + conversation,top_p=person.INTELLIGENCE)
        memory_description = response.choices[0].message.content

        # create a new concept node

        # what should node ID be? create? amount? poigancy?
        # how long should memory_description be?

        node = ConceptNode(-1, "chat", -1, person.attributes["id"], "chat with", individuals_ids, -1, memory_description, -1)
        person.memorystream.add_concept_node(node)











