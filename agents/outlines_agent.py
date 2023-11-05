from typing import Callable, List

import bs4
import outlines.text as text
from .agent import Agent


@text.prompt
def build_prompt(name: str, message_history: List[str], phase: str):
    """You are {{name}} who is playing a social deduction game with your friends.
    Your task is to continue the conversation as {{name}} and remember to follow the guide of the moderator.
    This is what has transpired in the conversation so far:

    {% for message in message_history %}
    {{message}}
    {% endfor %}

    {% if phase == "VOTING" %}
    Note: Put the name of the agent you want to vote for in the xml tag <message></message>. For example, <message>Agent A</message>.
    {% elif phase == "GUESSING" %}
    Note: Put the keyword you want to guess in the xml tag <message></message>. For example, <message>keyword</message>.
    {% else %}
    Note: Wrap your message to the group with xml tag like this <message>your message</message>.
    {% endif %}

    {{name}}:"""


class OutlinesAgent(Agent):
    """
    Agent that uses the outlines model to generate responses.

    Attributes:
        name (str): The name of the agent.
        llm (Callable): The outlines model.
    """
    def __init__(self, name: str, llm: Callable) -> None:
        """
        Initializes a new Agent instance.

        Args:
            name (str): The name of the agent.
            llm (Callable): The outlines model.

        Returns:
            None
        """
        super().__init__(name)
        self.llm = llm

    def act(self, message_history: List[str], phase: str) -> str:
        """
        Perform an action based on the given message history and phase.

        Args:
            message_history (List[str]): A list of previous messages.
            phase (str): The current phase of the agent.

        Returns:
            str: The action to be taken by the agent.
        """
        prompt = build_prompt(name=self.name, message_history=message_history, phase=phase)
        raw_action = self.llm(prompt)
        parsed_result = self._parse_raw_action(raw_action, tag="message")
        if parsed_result:
            action = parsed_result.text
        else:
            action = "I have nothing to say."
        return action

    def _parse_raw_action(self, raw_action: str, tag: str = "message") -> bs4.element.Tag:
        """
        Parse the raw action and extract the text content of the tag

        Args:
            raw_action (str): A string containing XML tags representing the raw action.
            tag (str): The tag to be extracted from the raw action.

        Returns:
            
        """
        parser = bs4.BeautifulSoup(raw_action, "html.parser")
        return parser.find(tag)