from agt_server.agents.base_agents.chicken_agent import ChickenAgent
from agt_server.local_games.chicken_arena import ChickenArena
import argparse


class BasicAgent(ChickenAgent):
    def setup(self):
        self.SWERVE, self.CONTINUE = 0, 1
        self.actions = [self.SWERVE, self.CONTINUE]
        self.round = 0

    def get_action(self):
        if self.round % 3 == 0:
            return self.CONTINUE
        else:
            return self.SWERVE

    def update(self):
        self.round += 1
