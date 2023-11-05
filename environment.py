class Environment:
    """
    Environment for the game Undercover.

    Args:
        agents (List[str]): A list of agents participating in the game.
        keyword_pair (Tuple[str]): A tuple containing the two keywords for the game.

    Attributes:
        agents (List[str]): A list of agents participating in the game.
        keyword_pair (Tuple[str]): A tuple containing the two keywords for the game.
        current_agent_index (str): Index of the current agent.
        game_phase (GamePhase): The current phase of the game.

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
        pass

    def reset(self) -> None:
        """
        Resets the environment to its initial state.

        Returns:
            None
        """
        pass

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
        pass

    def _check_terminal(self) -> bool:
        """
        Checks if the game is in a terminal state.

        Returns:
            bool: True if the game is in a terminal state, False otherwise.
        """
        pass

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
        pass

    def _moderator_announce(self, message: str, receiver: Union[List[str], str] = []) -> None:
        """
        Announces a message from the moderator to the specified receiver(s).

        Args:
            message (str): The message to be announced.
            receiver (Union[List[str], str], optional): The receiver(s) of the message. Defaults to [].

        Returns:
            None
        """
        pass

