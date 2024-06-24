import numpy as np
from Logic.game import Game
from Logic.reward_functions import *

class Agent:
    def __init__(self, id, stake, threshold_value, reward_function):
        self.id = id
        self.stake = stake
        self.threshold_value = threshold_value
        self.action_history = []
        self.pool = 0
        self.reward_function = reward_function

    def take_action(self, action):
        self.action_history.append(action)
        self.pool = action
    
    def choose_action(self, agents):
        # The agent needs to select one of the m pools to put their stake to.
        # We calculate the Shapley Value for each pool and the next action will
        #  be the one that has the highest Shapley value.
        agents_action = np.array([agent.pool for agent in agents])
        pools = np.where(agents_action == np.arange(len(agents_action)))[0]

        best_val = float('-inf')
        best_response = 0
        for pool in pools:
            curr_agents = agents[np.where(agents_action == pool)[0]]
            if self.pool != pool: curr_agents = np.append(curr_agents, self)

            game = Game(curr_agents)
            curr_val = self.reward_function.get_value(game, self.id)

            if curr_val > best_val:
                best_val = curr_val
                best_response = pool

        self.take_action(best_response)
        return best_response
    
    def __str__(self):
        return f'ID: {self.id} with total stake {self.stake}'