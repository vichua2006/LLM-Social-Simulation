from typing import List, Optional
from autogen import AssistantAgent
from Main.Individual import Individual
from Main.Query import generate_environment_description, generate_general_description
from Main.System import System
from Main.Retrieve import new_retrieve


def converse(individuals: List[Individual], system: System, chat_topic: str, temp_personalities: List[str]) -> str:
    '''
    initiate a conversation between individuals with AutoGen GroupChat
    returns the conversation content as a json string

    chat_topic: a string describing the topic of discussion for this groupchat. It will be used to retrieve relevant memories

    temp_personalities is a temporary variable to pass in the personality descriptions (big 5) of each individual; not sure how it should be done
    '''

    # udpate the system message of each agent with game rules/ setting, retrieved memory, personality (incomplete), pleasure system output (not implemented), and personal status (not implemented)
    for person in individuals:

        environment_description = generate_environment_description()
        general_description = generate_general_description(person, system)

        retrieved_memories = new_retrieve(person, )




