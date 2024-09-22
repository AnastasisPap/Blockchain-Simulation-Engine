import numpy as np
from scipy.stats import norm
from Logic.game import Game

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
        # We calculate the reward for each pool and the next action will
        #  be the one that has the highest value.
        agent_actions = np.array([agent.pool for agent in agents])
        pools = np.where(agent_actions == np.arange(len(agent_actions)))[0]

        # W stores the weights of the agents for each pool created and also
        # includes the current agent's stake for each pool, if not already.
        W = np.zeros((len(pools), len(agents)))
        for i, pool in enumerate(pools):
            idxes = np.where(agent_actions == pool)[0]
            if self.pool != pool: idxes = np.append(idxes, self.id)

            W[i, idxes] = np.array([agent.stake for agent in agents[idxes]])
        
        # Calculate the Shapley Value for each agent for all the pools
        sols = self.reward_function.get_value(self, W)

        best_response = pools[np.argmax(sols)]
        self.take_action(best_response)

        return best_response

    def __str__(self):
        return f'ID: {self.id} with total stake {self.stake}'