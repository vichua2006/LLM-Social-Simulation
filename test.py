# Importing necessary libraries
import autogen
import json

# api key
KEY = "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"

speak_for_yourself_msg = """DO NOT GENERATE RESPONSES FOR OTHER AGENTS, ONLY SPEAK FOR YOURSELF."""

terminate_chat_when_agreed_msg = """When everyone in the conversation has formed an agreement on a topic, reply "TERMINATE" """

speak_for_yourself = True
terminate_chat_when_agreed = True

system_msg = f"""
[System Note: 
{speak_for_yourself_msg if speak_for_yourself else ""} 
{terminate_chat_when_agreed_msg if terminate_chat_when_agreed else ""}
]
"""

# preferably use config_list_from_json to set config list
# eventually os.environ.get()
config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": KEY,
    },  
]
# refer to this notebook for full code examples of the different methods.
# https://github.com/microsoft/autogen/blob/main/notebook/oai_openai_utils.ipynb


llm_config = {
    "config_list": config_list, 
    "temperature": 0.0, 
}

agent_memories = [
    "You are in a virtual social scenerio where you are a farmer.You farm land to get food and You need a policy that prone to the production and selling of food.",
    "You are in a virtual social scenerio where you are a good producer. You produce luxury goods. You need policy that prone to the production and selling of luxury good.",
    "You are in a virtual social scenerio where you are a good producer. You produce luxury goods. You have been robbed a lot by other people, and you want that to stop.",
    "You are in a virtual social scenerio where you are a farmer.You farm land to get food, but you really enjoy luxury goods and want more of it.",
    "You are in a virtual social scenerio where you are a farmer.You farm land to get food, but you were robbed of your land can no longer farm for food, so you wish for a policy that increases trade.",
]

# initialize agents with different prompts
agents = [autogen.AssistantAgent(name=f"Agent_{i}", system_message=memory + " Your name is agent_{i}." + system_msg, llm_config=llm_config) for i, memory in enumerate(agent_memories, 1)]

# define group chat
groupchat = autogen.GroupChat(agents=agents, messages=[], max_round=100)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# initiate chat with the first 

agents[0].initiate_chat(manager, message="system message: Now, several members of the social scenerio have gathered to discuss their thoughts on a policy that their master implemented which prioritized food production. Limit each response to 50 words.")

# outputs all responses as a list of json objects to be passed on to the soverign

# print(json.dumps(manager.chat_messages[agents[0]], indent=4))

print(json.dumps(groupchat.messages, indent=4))

# both methods are reliable, the groupchat arguably more
