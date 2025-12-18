from q_learning import QLearning
from agt_server.local_games.lemonade_arena import LemonadeArena
from agt_server.agents.test_agents.lemonade.stick_agent.my_agent import StickAgent
from agt_server.agents.test_agents.lemonade.always_stay.my_agent import ReserveAgent
from agt_server.agents.test_agents.lemonade.decrement_agent.my_agent import DecrementAgent
from agt_server.agents.test_agents.lemonade.increment_agent.my_agent import IncrementAgent


class MyRLAgent(QLearning):
    def __init__(self, name, num_possible_states, num_possible_actions, initial_state, learning_rate, discount_factor, exploration_rate, training_mode, save_path=None) -> None:
        super().__init__(name, num_possible_states, num_possible_actions, initial_state,
                         learning_rate, discount_factor, exploration_rate, training_mode, save_path)
        
        # NOTE: Feel Free to edit Setup or Get Action in q_learning.py for further customization or simply even build a q-learning
        #       agent from scratch in my_agent.py

    def determine_state(self):
        # Determines the next state s_prime given the action histories and reward histories
        my_action_hist = self.get_action_history()
        my_util_hist = self.get_util_history()
        opp1_action_hist = self.get_opp1_action_history()
        opp2_action_hist = self.get_opp2_action_history()
        
        
        # TODO: Fill out this function
        m = 1
        state = 0
        for action in opp1_action_hist[-1:]:
            state += m * action
            m *= NUM_POSSIBLE_ACTIONS
        for action in opp2_action_hist[-1:]:
            state += m * action
            m *= NUM_POSSIBLE_ACTIONS
        return state

# TODO: Give your agent a NAME 
name = "PLEASE NAME ME D:"


# TODO: Determine how many states that your agent will be using
NUM_POSSIBLE_STATES = 144
INITIAL_STATE = 0


# Lemonade as 12 possible actions [0 - 11]
NUM_POSSIBLE_ACTIONS = 12
LEARNING_RATE = 0.05
DISCOUNT_FACTOR = 0.90
EXPLORATION_RATE = 0.05

################### SUBMISSION #####################
rl_agent_submission = MyRLAgent(name, NUM_POSSIBLE_STATES, NUM_POSSIBLE_ACTIONS,
                                   INITIAL_STATE, LEARNING_RATE, DISCOUNT_FACTOR, EXPLORATION_RATE, False, "my-qtable.npy")
####################################################

if __name__ == "__main__":
    rl_agent_submission.set_training_mode(True)
    if rl_agent_submission.training_mode: 
        print("TRAINING PERFORMANCE")
        arena = LemonadeArena(
            num_rounds=100000,
            timeout=1,
            players=[
                rl_agent_submission,
                StickAgent("Bug1"),
                StickAgent("Bug2"),
                StickAgent("Bug3"),
                StickAgent("Bug4")
            ]
        ) # NOTE: FEEL FREE TO EDIT THE AGENTS HERE TO TRAIN AGAINST A DIFFERENT DISTRIBUTION OF AGENTS. A COUPLE OF EXAMPLE AGENTS
          # TO TRAIN AGAINST ARE IMPORTED FOR YOU. 
        arena.run()
    print("TESTING PERFORMANCE")
    rl_agent_submission.set_training_mode(False)
    arena = LemonadeArena(
        num_rounds=1000,
        timeout=1,
        players=[
            rl_agent_submission,
            StickAgent("Bug1"),
            StickAgent("Bug2"),
            StickAgent("Bug3"),
            StickAgent("Bug4")
        ]
    )
    # NOTE: FEEL FREE TO EDIT THE AGENTS HERE TO TEST AGAINST A DIFFERENT DISTRIBUTION OF AGENTS. A COUPLE OF EXAMPLE AGENTS
    #       TO TEST AGAINST ARE IMPORTED FOR YOU. 
    arena.run()