from abc import ABC, abstractmethod
from typing import List

class Agent(ABC):
    """
    An abstract class for an agent in the game.

    Attributes:
        name (str): The name of the agent.
    """
    def __init__(self, name: str) -> None:
        """
        Initializes a new Agent instance.

        Args:
            name (str): The name of the agent.

        Returns:
            None
        """
        self.name = name

    @abstractmethod
    def act(self, message_history: List[str], phase: str) -> str:
        """
        Perform an action based on the given message history and phase.

        Args:
            message_history (List[str]): A list of previous messages.
            phase (str): The current phase of the agent.

        Returns:
            str: The action to be taken by the agent.
        """
        pass