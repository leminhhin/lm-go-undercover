import random
from typing import List, Tuple, Optional
from utils import MessagePool, VoteManager, GamePhase, GameRole

NUM_TO_ROLES = {
    # num of agents: (num of civilian, num of undercover, num of mr.white)
    3: [2, 1, 0],
    4: [3, 1, 0],
    5: [3, 1, 1],
    6: [4, 1, 1],
    7: [4, 2, 1],
}

class Environment:
    """
    Environment for the game Undercover.

    Args:
        agents (List[str]): A list of agents participating in the game.
        keyword_pair (Tuple[str]): A tuple containing the two keywords for the game.

    Attributes:
        initial_agents (List[str]): A list of agents participating in the game.
        agents (List[str]): A list of alive agents.
        role_to_keyword (Dict[GameRole, str]): A dictionary mapping game roles to keywords.
        current_agent_index (str): Index of the current agent.
        phase (GamePhase): The current phase of the game.
        message_pool (MessagePool): The message pool containing all the messages sent in the game.
        vote_manager (VoteManager): The vote manager managing the votes in the game.
        terminal (bool): True if the game is in a terminal state, False otherwise.
        role_to_agents (Dict[GameRole, List[str]]): A dictionary mapping game roles to agents.
    """

    def __init__(self, agents: List[str], keyword_pair: Tuple[str]) -> None:
        """
        Initializes the environment with the given list of agents and keyword pair.

        Args:
            agents (List[str]): A list of agents participating in the game.
            keyword_pair (Tuple[str]): A tuple containing the two keywords for the game.

        Returns:
            None
        """
        # Check if the number of agents is between 3 and 7
        assert 3 <= len(agents) <= 7, "Number of agents must be between 3 and 7."

        # Set the initial agents and create a copy as the alive agents
        self.initial_agents = agents
        self.agents = self.initial_agents.copy()

        # Create a dictionary mapping game roles to keywords
        self.role_to_keyword = {
            GameRole.CIVILIAN: keyword_pair[0],
            GameRole.UNDERCOVER: keyword_pair[1],
        }

        # Initialize the game state variables
        self.current_agent_index = 0
        self.phase = None
        self.message_pool = None
        self.vote_manager = None
        self.terminal = None
        self.role_to_agents = None

        # Call the reset method to reset the environment to its initial state
        self.reset()

    def reset(self) -> None:
        """
        Resets the environment to its initial state.

        Returns:
            None
        """
        self.agents = self.initial_agents.copy()
        self.current_agent_index = 0
        self.message_pool = MessagePool()
        self.vote_manager = VoteManager(self.agents)
        self.terminal = False
        self._assign_roles()

        self._moderator_announce("The game Undercover starts!")

        civilians = self.role_to_agents[GameRole.CIVILIAN]
        self._moderator_announce(
            f"Your role is civilian. Your keyword is *{self.role_to_keyword[GameRole.CIVILIAN]}*. Your goal is to find other civilians, eliminate the undercover and Mr. White, while keeping your role and keyword unrevealed.",
            civilians,
        )

        undercovers = self.role_to_agents[GameRole.UNDERCOVER]
        self._moderator_announce(
            f"Your role is undercover. Your keyword is *{self.role_to_keyword[GameRole.UNDERCOVER]}*. Your goal is to blend in, survive till the end, while keeping your role and keyword unrevealed.",
            undercovers,
        )

        mr_white = self.role_to_agents[GameRole.MRWHITE]
        self._moderator_announce(
            "Your role is Mr. White. You do not have a keyword. Your goal is to blend in, survive till the end, keeping your role unrevealed and try to catch the civilian's keyword.",
            mr_white,
        )

        self._update_phase(GamePhase.DESCRIPTION)

    def step(self, agent: str, action: str) -> None:
        """
        Takes a step in the environment, updating the game state.

        Args:
            agent (str): The agent taking the step.
            action (str): The action taken by the agent.

        Returns:
            None
        """
        pass

    def get_current_agent(self) -> str:
        """
        Returns the current agent.

        Returns:
            str: The current agent.
        """
        pass

    def export(self, path: str) -> None:
        """
        Exports the environment to a file at the specified path, including the game setting and game conversation.

        Args:
            path (str): The path to export the environment.

        Returns:
            None
        """
        with open(path, "w", encoding="utf-8") as f:
            export_string = "----------Game Setting----------\n"
            export_string += f"Agents: {self.initial_agents}\n"
            export_string += f"Roles: {self.role_to_agents}\n"
            export_string += f"Civilian keyword: {self.role_to_keyword[GameRole.CIVILIAN]}\n"
            export_string += f"Undercover keyword: {self.role_to_keyword[GameRole.UNDERCOVER]}\n"
            export_string += "\n\n"

            export_string += "----------Conversation----------\n"
            for message in self.message_pool.messages:
                export_string += f"{message.sender} -> {message.receiver}: {message.content}\n"

            f.write(export_string)

    def _check_terminal(self) -> List[bool]:
        """
        Checks if the game is in a terminal state.

        Returns:
            List[bool]: A list of booleans indicating if each role wins.
        """
        alive_agents = {role: 0 for role in GameRole}
        for agent in self.agents:
            for role, agents in self.role_to_agents.items():
                if agent in agents:
                    alive_agents[role] += 1

        num_alive_civilian = alive_agents[GameRole.CIVILIAN]
        num_alive_undercover = alive_agents[GameRole.UNDERCOVER]
        num_alive_mrwhite = alive_agents[GameRole.MRWHITE]

        role_to_terminal = {role: False for role in GameRole}
        if num_alive_undercover + num_alive_mrwhite == 0:
            role_to_terminal[GameRole.CIVILIAN] = True
        elif num_alive_civilian <= 1:
            if num_alive_undercover > 0 and num_alive_mrwhite > 0:
                role_to_terminal[GameRole.UNDERCOVER] = True
                role_to_terminal[GameRole.MRWHITE] = True
            elif num_alive_undercover > 0:
                role_to_terminal[GameRole.UNDERCOVER] = True
            elif num_alive_mrwhite > 0:
                role_to_terminal[GameRole.MRWHITE] = True

        return role_to_terminal

    def _update_phase(self, new_phase: GamePhase) -> None:
        """
        Updates the game phase to the specified phase.

        Args:
            new_phase (GamePhase): The new phase of the game.

        Returns:
            None
        """
        pass
    
    def _assign_roles(self) -> None:
        """
        Assigns roles to the agents.

        Returns:
            None
        """
        num_agents = len(self.initial_agents)
        num_civilian, num_undercover, num_mrwhite = NUM_TO_ROLES[num_agents]
    
        roles = [GameRole.CIVILIAN] * num_civilian + [GameRole.UNDERCOVER] * num_undercover + [GameRole.MRWHITE] * num_mrwhite
        random.shuffle(roles)
    
        self.role_to_agents = {role: [] for role in [GameRole.CIVILIAN, GameRole.UNDERCOVER, GameRole.MRWHITE]}
    
        for agent, role in zip(self.agents, roles):
            self.role_to_agents[role].append(agent)

    def _moderator_announce(self, message: str, receiver: Optional[List[str]] = None) -> None:
        """
        Announces a message from the moderator to the specified receiver(s).

        Args:
            message (str): The message to be announced.
            receiver (Union[List[str], str], optional): The receiver(s) of the message. Defaults to None.

        Returns:
            None
        """
        if receiver is None:
            receiver = self.agents
        elif len(receiver) == 0:
            return
        else:
            pass

        self.message_pool.add_message("Moderator", message, receiver)

