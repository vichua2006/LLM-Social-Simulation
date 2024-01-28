from typing import Optional, Union, List, Dict, Literal, Callable
from autogen import ConversableAgent, GroupChat
from autogen.agentchat.agent import Agent

#included in individual file to resolve 
class SpeakingAgent(ConversableAgent):

    def __init__(
        self,
        name: str,
        system_message: Optional[Union[str, List]] = "You are a helpful AI Assistant.",
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "TERMINATE",
        function_map: Optional[Dict[str, Callable]] = None,
        code_execution_config: Optional[Union[Dict, Literal[False]]] = None,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        default_auto_reply: Optional[Union[str, Dict, None]] = "",
        description: Optional[str] = None,
    ):
        '''redefining constructor to add personality variable'''
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            function_map,
            code_execution_config=code_execution_config,
            llm_config=llm_config,
            default_auto_reply=default_auto_reply,
            description=description,
        )

        self.personality = ""
    
    def update_personality(self, description: str) -> None:
        '''
        updates the agent's personality variable 
        '''
        self.personality = description


class CustomGroupChat(GroupChat):
    '''
    overrode one method to include agent personality in speaker selection
    '''

    def select_speaker_prompt(self, agents: Optional[List[SpeakingAgent]] = None) -> str:
        """This is always the *last* message in the context. The personality of each agent is appended to the end of the message, and the LM is told to consider their personalities"""
        if agents is None:
            agents = self.agents
        
        priorities = "\n".join([f"{agent.name} : {agent.personality}" for agent in agents])
    
        statement = f'''
        Read the above conversation and consider the label of each role. Then select the next role from {[agent.name for agent in agents]} to play.

        Select them in somewhat random fashion. Not every role has to be selected.
        Here are the labels of each role: 
        {priorities}
        OFTEN select roles labeled as FREQUENT.
        OCCASIONALLY select roles labeled as SOMETIMES
        ALMOST NEVER select the roles labeled as SELDOM.

        Only return the role.
        '''

        return statement

    def select_speaker_msg(self, agents: List[Agent]) -> str:
        return super().select_speaker_msg(agents)