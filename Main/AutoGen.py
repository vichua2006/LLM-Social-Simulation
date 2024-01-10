from autogen import AssistantAgent

################# TEMPORARY #######################
# Not sure how api keys and config want to be handled

victor_key = "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"

config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": victor_key,
    },  
]

llm_config = {
    "config_list": config_list, 
    "temperature": 0.0, 
}

#####################################################

def termination_function():
    # this function gets passed to GroupChatManager to determine when chatting terminates
    # currently does nothing
    pass

def initialize_agent(name: str) -> AssistantAgent:
    # this function initializes an AssistantAgent instance with the configurations in this file
    # the system message is left blank; it will be updated before agents converse
    return AssistantAgent(name=name, system_message="", llm_config=llm_config)