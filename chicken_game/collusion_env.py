import random
import numpy as np
import matplotlib.pyplot as plt

class CollusionEnv():
    def __init__(self, agents, num_tot_actions, num_tot_states) -> None:
        self.agents = agents 
        self.num_tot_actions = num_tot_actions
        self.num_tot_states = num_tot_states
    
    def run(self, save_figs = True): 
        random.seed(456)
        # We generate random prices to provide initial observation to Q learners
        num_tot_actions = self.num_tot_actions
        agents = self.agents
        agent1, agent2 = agents
        random_actions = [random.randint(0, num_tot_actions - 1), random.randint(0, num_tot_actions - 1)]
        agent1.my_action_hist.append(random_actions[0])
        agent1.opp_action_hist.append(random_actions[1])
        agent1.s = agent1.determine_state()
        agent1.choose_next_move(step = 0)
        
        agent2.my_action_hist.append(random_actions[1])
        agent2.opp_action_hist.append(random_actions[0])
        agent2.s = agent2.determine_state()
        agent2.choose_next_move(step = 0)

        actions = np.array([agent1.a, agent2.a])

        step = 0
        while step < agent1.max_steps:
            # Increment and print step count every 100000 steps
            step += 1
            if step % 100000 == 0:
                print("Steps completed: ", step)

            agent1.my_action_hist.append(actions[0])
            agent1.opp_action_hist.append(actions[1])
            agent2.my_action_hist.append(actions[1])
            agent2.opp_action_hist.append(actions[0])
            old_states = [agent1.determine_state(), agent2.determine_state()]
            for i, agent in enumerate(agents):
                agent.choose_next_move(step = step)
                actions[i] = agent.a

            agent1.my_action_hist.append(actions[0])
            agent1.opp_action_hist.append(actions[1])
            agent2.my_action_hist.append(actions[1])
            agent2.opp_action_hist.append(actions[0])
            
            prices = agent1.action_price_space.take(
                actions)  # Convert actions into prices

            # Compute rewards at current prices
            rewards = {}
            for i, agent in enumerate(agents):
                demand_i = np.exp((agent.a_i - prices[i]) / agent.mu) / (
                    np.sum(np.exp((agent.a_i - prices) / agent.mu)) + np.exp(agent.a_0 / agent.mu))
                rewards[i] = (prices[i] - agent.c_i) * demand_i

            # Update agents' tables and check convergence a la Johnson et al. 2021
            old_optimal_actions = [
                np.argmax(agents[i].q[:, old_states[i]]) for i in range(2)]
            for i in range(2):
                agents[i].transition(rewards[i], step)
            agent1.my_action_hist.append(agent1.a)
            agent1.opp_action_hist.append(agent2.a)
            agent2.my_action_hist.append(agent2.a)
            agent2.opp_action_hist.append(agent1.a)
            
            has_converged = agent1.check_if_converged(old_optimal_actions, step)

            if has_converged:
                break

        # Generate equilibrium price trajectory
        prices = []

        for _ in range(10):
            for i, agent in enumerate(agents):
                agent.choose_next_move(step = step)
                actions[i] = agent.a
            agent1.my_action_hist.append(actions[0])
            agent1.opp_action_hist.append(actions[1])
            agent2.my_action_hist.append(actions[1])
            agent2.opp_action_hist.append(actions[0])
            prices.append(agent1.action_price_space.take(actions))

        x = range(len(prices))
        y1 = [price[0] for price in prices]
        y2 = [price[1] for price in prices]

        fig, ax = plt.subplots()
        ax.plot(x, y1, 'o-', label='price_1')
        ax.plot(x, y2, 'o-', label='price_2')
        ax.axhline(y=1.45, color='red', linestyle='--', label='Bertrand price')
        ax.axhline(y=1.95, color='green', linestyle='--', label='Monopoly price')
        ax.legend()
        plt.title("Equilibrium price trajectory")
        if save_figs: 
            plt.savefig("figures/Equilibrium price trajectory")
        plt.show()
        

        # Test punishment if first agent deviates and prices at Nash
        actions[0] = 0
        agent1.my_action_hist[-1] = actions[0]
        agent2.opp_action_hist[-1] = actions[0]
        prices_after_deviation = []

        for _ in range(10):
            prices_after_deviation.append(agent1.action_price_space.take(actions))
            for i, agent in enumerate(agents):
                agent.choose_next_move(step)
                actions[i] = agent.a
            agent1.my_action_hist.append(actions[0])
            agent1.opp_action_hist.append(actions[1])
            agent2.my_action_hist.append(actions[1])
            agent2.opp_action_hist.append(actions[0])
            

        x = range(len(prices_after_deviation))
        y1 = [price[0] for price in prices_after_deviation]
        y2 = [price[1] for price in prices_after_deviation]

        fig, ax = plt.subplots()
        ax.plot(x, y1, 'o-', label='price_1')
        ax.plot(x, y2, 'o-', label='price_2')
        ax.axhline(y=1.45, color='red', linestyle='--', label='Bertrand price')
        ax.axhline(y=1.95, color='green', linestyle='--', label='Monopoly price')
        ax.legend()
        plt.title("Punishment if Deviation")
        if save_figs: 
            plt.savefig("figures/Punishment if Deviation")
        plt.show()
        

        plt.plot(agent1.eps)
        plt.title("Exploration Rate over time")
        if save_figs: 
            plt.savefig("figures/Exploration Rate over time")
        plt.show()
        
        