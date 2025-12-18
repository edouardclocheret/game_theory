from my_rl_lemonade_agent import rl_agent_submission 
from my_lemonade_agent import nrl_agent_submission 
from agt_server.agents.base_agents.lemonade_agent import LemonadeAgent
from agt_server.local_games.lemonade_arena import LemonadeArena
from agt_server.agents.test_agents.lemonade.stick_agent.my_agent import StickAgent
from agt_server.agents.test_agents.lemonade.always_stay.my_agent import ReserveAgent
from agt_server.agents.test_agents.lemonade.decrement_agent.my_agent import DecrementAgent
from agt_server.agents.test_agents.lemonade.increment_agent.my_agent import IncrementAgent

class MyAgent(LemonadeAgent):
    def setup(self):
        pass

    def get_action(self):
        raise NotImplementedError

    def update(self):
        pass
    

# TODO: Give your agent a NAME 
name = "PLEASE NAME ME D:"

################### SUBMISSION #####################
# TODO: Set to your RL Agent by default, change it to whatever you want as long as its a agent that inherits LemonadeAgent
agent_submission = rl_agent_submission
################### SUBMISSION #####################

if __name__ == "__main__":
    arena = LemonadeArena(
        num_rounds=1000,
        timeout=1,
        players=[
            agent_submission,
            StickAgent("Bug1"),
            StickAgent("Bug2"),
            StickAgent("Bug3"),
            StickAgent("Bug4")
        ]
    )
    # NOTE: FEEL FREE TO EDIT THE AGENTS HERE TO TEST AGAINST A DIFFERENT DISTRIBUTION OF AGENTS. A COUPLE OF EXAMPLE AGENTS
    #       TO TEST AGAINST ARE IMPORTED FOR YOU. 
    arena.run()