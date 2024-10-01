import numpy as np
import warnings
from scipy.stats import norm
from more_itertools import powerset

class RewardFunctions:
    def __init__(self, selection, extra_args=[]):
        """
        Args:
          - selection (int): contains an integer that represents which
            reward function has been selected (set in the cmd arguments).
          - extra_args (list): contains extra arguments that are needed,
            for example m which is the number of samples for MC approx.
        """
        self.selection = selection
        self.extra_args = extra_args

    def get_value(self, agent, W):
        """
        Args:
        - agent (Agent): the current agent for which we want to calculate the value
        - W (np.array): the matrix with shape (# pools, # agents) of weights for the pools
        Returns:
        - np.array: np array with # pools entries, which correspond to the value of
            the agent for each pool
        """
        if self.selection == 0:
            return self.exact_shap(agent, W)
        elif self.selection == 1:
            return self.wvg_shap(agent, W)
        else:
            raise Exception("Incorrect option for Reward Function.")

    def get_utility(self, stake, coalition_stake, threshold):
        return int(coalition_stake + stake >= threshold) - int(coalition_stake >= threshold)

    def exact_shap(self, curr_agent, W):
        """Compute the exact Shapley value
        """
        coefficients = np.zeros(W.shape[1])
        shap_values = np.zeros(W.shape[0])

        for pool in range(W.shape[0]):
            curr_agents = set(np.where(W[pool, :] > 0)[0])
            n = len(curr_agents)
            subsets = list(powerset(curr_agents - set([curr_agent.id])))
            exact_sv = 0

            for i in range(n):
                coefficients[i] = np.math.factorial(n-i-1) * np.math.factorial(i) / np.math.factorial(n)

            for subset in subsets:
                curr_stakes = W[pool, list(subset)]
                exact_sv += coefficients[len(subset)] * self.get_utility(curr_agent.stake, np.sum(curr_stakes), curr_agent.threshold_value)
            
            shap_values[pool] = exact_sv
        
        return shap_values

    # Taken from: "A linear approximation method for the Shapley value"
    #     by Fatima, Wooldridge, Jennings. Used for Weighted Voting Games.
    def wvg_shap(self, curr_agent, W):
        stake = curr_agent.stake
        q = curr_agent.threshold_value

        phi = np.zeros(W.shape[0])
        n = W.shape[1]

        for game in range(W.shape[0]):
            mu = float(np.mean(W[game, :]))
            var = float(np.var(W[game, :]))
            sigma_s = np.power(var / np.linspace(1, n - 1, n - 1), 0.5)
            a_s, b_s = (q-stake) / np.linspace(1, n - 1, n - 1), (q-10**-20) / np.linspace(1, n - 1, n - 1)

            shap_in_game = norm.cdf(b_s, loc=mu, scale=sigma_s) - norm.cdf(a_s, loc=mu, scale=sigma_s)
            phi[game] = np.sum(shap_in_game)
        
        phi = phi / n
        return phi