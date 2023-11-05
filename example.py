import os
from datetime import datetime
import time
import outlines.models as models

from agents.outlines_agent import OutlinesAgent
from environment import Environment

agents = [
    OutlinesAgent(name="Alice", llm=models.text_completion.openai(
            model_name="gpt-4",
            max_tokens=50,
            temperature=1)
    ),
    OutlinesAgent(name="Bob", llm=models.text_completion.openai(
            model_name="gpt-4",
            max_tokens=50,
            temperature=1)
    ),
    OutlinesAgent(name="Charlie", llm=models.text_completion.openai(
            model_name="gpt-4",
            max_tokens=50,
            temperature=1)
    ),
    OutlinesAgent(name="David", llm=models.text_completion.openai(
            model_name="gpt-4",
            max_tokens=50,
            temperature=1)
    ),
    OutlinesAgent(name="Eve", llm=models.text_completion.openai(
            model_name="gpt-4",
            max_tokens=50,
            temperature=1)
    ),
]
name_to_agent = {agent.name: agent for agent in agents}


# Initialize environment
env = Environment(
    agents=[agent.name for agent in agents],
    keyword_pair=["openai", "chatgpt"],
)

now = datetime.now().strftime("%Y%m%d%H%M%S")
os.makedirs("logs", exist_ok=True)

start = time.time()
# Start the game
for _ in range(65):
    agent_name = env.get_current_agent()
    agent = name_to_agent[agent_name]
    observation = [str(message) for message in env.message_pool.get_message(agent_name)]

    action = agent.act(observation, env.phase.name)
    env.step(agent_name, action)

    env.export(f"logs/{now}.txt")
    if env.terminal:
        break
    time.sleep(3)


end = time.time()
print(f"Time elapsed: {end - start}s")