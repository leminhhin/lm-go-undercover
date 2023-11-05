from enum import Enum
from typing import List, Optional


class GamePhase(Enum):
    """
    Enum class representing the different phases of the game.
    """
    DESCRIPTION = 0
    DISCUSSION = 1
    VOTING = 2
    GUESSING = 3


class GameRole(Enum):
    """
    Enum class representing the different roles in the game.
    """
    CIVILIAN = 0
    UNDERCOVER = 1
    MRWHITE = 2


class Message:
    """
    Represents a message sent from a sender to one or more receivers.

    Attributes:
        sender (str): The sender of the message.
        content (str): The content of the message.
        receiver (List[str]): The list of receivers of the message.
    """

    def __init__(
        self, sender: str, content: str, receiver: List[str]
    ) -> None:
        self.sender = sender
        self.content = content
        self.receiver = receiver

    def __str__(self) -> str:
        return f"{self.sender}: {self.content}"

    def __repr__(self) -> str:
        return str(self)


class MessagePool:
    """
    A class representing a pool of messages.

    Attributes:
        messages (List[Message]): The list of messages in the pool.
    """

    def __init__(self, messages: Optional[List[Message]] = None) -> None:
        """
        Initializes a MessagePool object.

        Args:
            messages (Optional[List[Message]]): Optional list of messages to initialize the pool with. Defaults to None.
        """
        if not messages:
            messages = []
        self.messages = messages

    def add_message(self, sender: str, message: str, receiver: List[str]) -> None:
        """
        Adds a new message to the pool.

        Args:
            sender (str): The sender of the message.
            message (str): The content of the message.
            receiver (List[str]): The list of receivers for the message.
        """
        self.messages.append(Message(sender, message, receiver))

    def get_message(self, receiver: Optional[str] = None) -> List[Message]:
        """
        Retrieves messages from the pool.

        If no receiver is specified, returns all messages.
        If a receiver is specified, returns messages that are either received by the specified receiver or sent by the specified receiver.

        Args:
            receiver (Optional[str]): The receiver of the messages. Defaults to None.

        Returns:
            List[Message]: The list of messages.
        """
        if not receiver:
            return self.messages
        messages = []
        for message in self.messages:
            if (
                receiver in message.receiver  # if message's receiver is receiver
                or message.sender == receiver  # or message is sent by receiver
            ):
                messages.append(message)
        return messages

class VoteManager:
    """
    A class that manages votes from different agents.

    Attributes:
        votes (dict): A dictionary that stores the vote count for each agent.
    """

    def __init__(self, agents: List[str]) -> None:
        """
        Initializes the VoteManager object with a list of agents.

        Args:
            agents (List[str]): A list of agent names.

        Returns:
            None
        """
        self.votes = {
            agent.strip().capitalize(): 0 for agent in agents
        }
    
    def add_vote(self, agent: str) -> None:
        """
        Adds a vote for a specific agent.

        Args:
            agent (str): The name of the agent.

        Returns:
            None
        """
        agent = agent.strip().capitalize()
        if agent in self.votes:
            self.votes[agent] += 1

    def get_eliminated_agent(self) -> str:
        """
        Returns the agent with the highest number of votes.

        Returns:
            str: The name of the agent with the highest number of votes.
        """
        return max(self.votes, key=self.votes.get)