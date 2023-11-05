<div align="center">

# LM Go Undercover

Let me / Language models go undercover

 [Game rules](#game-rules) | [Implementation](#implementation) | [Example Game](#example-game) | [Usage](#usage) | [Future Work](#future-work)

</div>

This project aims to simulate and analyze how LLMs play the social deduction game Undercover. The goal is to get a sense of how well LLMs can follow game rules, communicate effectively, and use strategy in a multiplayer environment.

## Game Rules

[Undercover](https://www.yanstarstudio.com) is an exciting and addictive social deduction word game to play with friends.

There are three roles:

- **Civilians**: Receive a secret keyword that is the same for all civilians. Make up a description of the keyword without giving it away.
- **Undercovers**: Receive a keyword that is similar but slightly different from the civilians' keyword. Describe their keyword while trying to blend in.
- **Mr. White**: Receives no keyword and must try to blend in with civilians.

The game has four phases:
- **Description Phase**: Each player describes their keyword without revealing the exact word.
- **Discussion Phase**: Players discuss the descriptions and try to deduce roles.
- **Voting Phase**: Everyone votes to eliminate who they believe are Undercovers or Mr. White. Undercovers want to eliminate Civilians.
- **Guessing Phase**: If Mr. White was eliminated, they guess the Civilians' secret word.

Civilians win if no Undercovers remain. Undercovers and Mr. White win if only 1 Civilian is left or if Mr. White guesses the secret word.

For more details, see [here](https://www.yanstarstudio.com/undercover-how-to-play).

## Implementation

### Agent-Environment Interaction

Agents interact with the environment and each other through an agent-environment cycle:

- The agent observes the environment by receiving a list of visible messages from the shared message pool. This serves as the agent's "memory".
- The agent takes an action by outputting a response. For LLM agents, this is a continuation prompt.
- The environment transitions state based on the agent's action and game rules.

**Action**: are agent responses and prompt continuations.

**Observation**: are lists of visible messages from the shared message pool.

### Message Pool

The message pool enables indirect agent-to-agent communication. It acts as a proxy that agents can use to exchange information.

When an agent takes an action, a message can be created from their response and added to the pool. Messages have specified receivers based on game rules or the agent's own choice.

The environment can also add moderator messages to provide game state info or instructions.

To generate an observation, the message pool collects all messages visible to an agent and returns them in a list.

## Example Game

The `example.py` script provides a simple demonstration of the game simulator with a sample conversation between 5 LLM agents.

The `logs/example.txt` file shows the message logs from an example game simulation. Some highlights:

## Usage

### Setup

1. Install requirements with:

```bash
pip install -r requirements.txt
```

2. Get an OpenAI API key and set it as an environment variable:

```bash
export OPENAI_API_KEY=YOUR_KEY_HERE
```

### Running the game

To see the game in action, run:

```bash
python example.py
```

This will simulate a full game with 5 LLM agents conversing.

Feel free to modify example.py as desired to customize the game simulation.

A standard 5 player game takes around 3-5 minutes to complete and costs 10K - 20K tokens, depending on the models, temperature, max_tokens used.

After a game finishes, you can view the conversation log in the /logs folder.

## Future Work

There are several areas for future improvement:

- **Prompt Optimization**: The current prompting strategy can be improved to get models to follow game rules more consistently. Prompts could also potentially be optimized to reduce cost.
- **Output Parsing**: The output parser is basic - more robust parsing would capture information more effectively.
- **Streaming Output**: Generating responses turn-by-turn limits real-time interaction. Integrating streaming APIs would enable smoother real-time gameplay.
- **Strategic Agents**: Agents currently lack long-term strategies, responding based only on prompt history. Incorporating planning algorithms would allow more intelligent play.

## Acknowledgements
- The class design and architecture for agent-environment cycle was inspired by [ChatArena](https://github.com/Farama-Foundation/chatarena/).
- This project simulates the social deduction game [Undercover](https://www.yanstarstudio.com), which I enjoy playing with friends. Check it out if you want to try the real game!
