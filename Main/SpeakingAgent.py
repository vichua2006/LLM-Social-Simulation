from typing import Optional, Union, List, Dict, Literal, Callable, Tuple, Any
from autogen import ConversableAgent, GroupChat, GroupChatManager
from autogen.agentchat.agent import Agent

# changing class method to reduce unnecessary text output (i.e. ">>>>>>>> USING AUTO REPLY...")
def new_check_termination_and_human_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[Any] = None,
    ) -> Tuple[bool, Union[str, None]]:
        """Check if the conversation should be terminated, and if human reply is provided.

        This method checks for conditions that require the conversation to be terminated, such as reaching
        a maximum number of consecutive auto-replies or encountering a termination message. Additionally,
        it prompts for and processes human input based on the configured human input mode, which can be
        'ALWAYS', 'NEVER', or 'TERMINATE'. The method also manages the consecutive auto-reply counter
        for the conversation and prints relevant messages based on the human input received.

        Args:
            - messages (Optional[List[Dict]]): A list of message dictionaries, representing the conversation history.
            - sender (Optional[Agent]): The agent object representing the sender of the message.
            - config (Optional[Any]): Configuration object, defaults to the current instance if not provided.

        Returns:
            - Tuple[bool, Union[str, Dict, None]]: A tuple containing a boolean indicating if the conversation
            should be terminated, and a human reply which can be a string, a dictionary, or None.
        """
        # Function implementation...

        if config is None:
            config = self
        if messages is None:
            messages = self._oai_messages[sender]
        message = messages[-1]
        reply = ""
        no_human_input_msg = ""
        if self.human_input_mode == "ALWAYS":
            reply = self.get_human_input(
                f"Provide feedback to {sender.name}. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: "
            )
            no_human_input_msg = "NO HUMAN INPUT RECEIVED." if not reply else ""
            # if the human input is empty, and the message is a termination message, then we will terminate the conversation
            reply = reply if reply or not self._is_termination_msg(message) else "exit"
        else:
            if self._consecutive_auto_reply_counter[sender] >= self._max_consecutive_auto_reply_dict[sender]:
                if self.human_input_mode == "NEVER":
                    reply = "exit"
                else:
                    # self.human_input_mode == "TERMINATE":
                    terminate = self._is_termination_msg(message)
                    reply = self.get_human_input(
                        f"Please give feedback to {sender.name}. Press enter or type 'exit' to stop the conversation: "
                        if terminate
                        else f"Please give feedback to {sender.name}. Press enter to skip and use auto-reply, or type 'exit' to stop the conversation: "
                    )
                    no_human_input_msg = "NO HUMAN INPUT RECEIVED." if not reply else ""
                    # if the human input is empty, and the message is a termination message, then we will terminate the conversation
                    reply = reply if reply or not terminate else "exit"
            elif self._is_termination_msg(message):
                if self.human_input_mode == "NEVER":
                    reply = "exit"
                else:
                    # self.human_input_mode == "TERMINATE":
                    reply = self.get_human_input(
                        f"Please give feedback to {sender.name}. Press enter or type 'exit' to stop the conversation: "
                    )
                    no_human_input_msg = "NO HUMAN INPUT RECEIVED." if not reply else ""
                    # if the human input is empty, and the message is a termination message, then we will terminate the conversation
                    reply = reply or "exit"

        # print the no_human_input_msg
        # if no_human_input_msg:
        #     print(colored(f"\n>>>>>>>> {no_human_input_msg}", "red"), flush=True)

        # stop the conversation
        if reply == "exit":
            # reset the consecutive_auto_reply_counter
            self._consecutive_auto_reply_counter[sender] = 0
            return True, None

        # send the human reply
        if reply or self._max_consecutive_auto_reply_dict[sender] == 0:
            # reset the consecutive_auto_reply_counter
            self._consecutive_auto_reply_counter[sender] = 0
            # User provided a custom response, return function and tool failures indicating user interruption
            tool_returns = []
            if message.get("function_call", False):
                tool_returns.append(
                    {
                        "role": "function",
                        "name": message["function_call"].get("name", ""),
                        "content": "USER INTERRUPTED",
                    }
                )

            if message.get("tool_calls", False):
                tool_returns.extend(
                    [
                        {"role": "tool", "tool_call_id": tool_call.get("id", ""), "content": "USER INTERRUPTED"}
                        for tool_call in message["tool_calls"]
                    ]
                )

            response = {"role": "user", "content": reply, "tool_responses": tool_returns}

            return True, response

        # increment the consecutive_auto_reply_counter
        self._consecutive_auto_reply_counter[sender] += 1
        # if self.human_input_mode != "NEVER":
        #     print(colored("\n>>>>>>>> USING AUTO REPLY...", "red"), flush=True)

        return False, None

# changing class method to reduce unnecessary text output (i.e. ">>>>>>>> USING AUTO REPLY...")
# directly changing method because overriding is too complicated
ConversableAgent.check_termination_and_human_reply = new_check_termination_and_human_reply

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
        '''redefining constructor to add speaking_tendency variable'''
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
            # description=description,
        )

        self.speaking_tendency = ""
    
    def send(
        self,
        message: Union[Dict, str],
        recipient: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        '''
        overrode method; silent is now true by default
        '''
        super().send(message, recipient, request_reply, silent)


    def update_speaking_tendency(self, tendency: str) -> None:
        '''
        updates the agent's speaking_tendency variable 
        '''
        self.speaking_tendency = tendency


class CustomGroupChat(GroupChat):
    '''
    overrode one method to include agent speaking tendency in speaker selection
    '''

    def select_speaker_prompt(self, agents: Optional[List[SpeakingAgent]] = None) -> str:
        """This is always the *last* message in the context. The speaking tendency of each agent is appended to the end of the message, and the LM is told to consider their personalities"""
        if agents is None:
            agents = self.agents
        
        tendencies = "\n".join([f"{agent.name} : {agent.speaking_tendency}" for agent in agents])
    
        statement = f'''
        Read the above conversation and consider the label of each role. Then select the next role from {[agent.name for agent in agents]} to play.
        You may only select roles that are in that list. DO NOT select roles that do not exists.

        Select them in somewhat random fashion. Every role has to be selected at least once.
        Here are the labels of each role: 
        {tendencies}
        OFTEN select roles labeled as FREQUENT.
        OCCASIONALLY select roles labeled as SOMETIMES
        ALMOST NEVER select the roles labeled as SELDOM.

        Only return the role.
        '''

        return statement

    def select_speaker_msg(self, agents: List[Agent]) -> str:
        return super().select_speaker_msg(agents)
    