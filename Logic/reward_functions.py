import numpy as np
import warnings
import scipy.stats as st
from more_itertools import powerset

class RewardFunctions:
    def __init__(self, selection, extra_args=[]):
        self.selection = selection
        self.extra_args = extra_args

    def get_value(self, game, agent_idx):
        args = (game, agent_idx)
        if self.selection == 0:
            return self.exact_shap(*args)
        elif self.selection == 1:
            return self.mc_shap(*args, *self.extra_args)
        elif self.selection == 2:
            return self.wvg_shap(*args, *self.extra_args)
        else:
            raise Exception("Incorrect option for Reward Function.")

    def exact_shap(self, game, agent_idx):
        """Compute the exact Shapley value
        """
        n = game.n
        exact_sv = 0
        coefficients = np.zeros(n)
        for i in range(n):
            coefficients[i] = np.math.factorial(n-1-i) * np.math.factorial(i) / np.math.factorial(n-1)

        subsets = list(powerset(game.get_agent_ids() - set([agent_idx])))
        for subset in subsets:
            exact_sv += coefficients[len(subset)] * game.utility(np.array(subset), agent_idx)

        return exact_sv / n

    def mc_shap(self, game, agent_idx, m):
        """Compute the Monte Carlo Shapley value by sampling m permutations
        """
        sv_approx = 0

        for iter in range(m):
            perm = np.random.permutation(list(game.get_agent_ids()))
            pre_of_agent = perm[:np.where(perm==agent_idx)[0][0]]
            sv_approx += game.utility(pre_of_agent, agent_idx)

        return sv_approx / m

    # Taken from: "A linear approximation method for the Shapley value"
    #     by Fatima, Wooldridge, Jennings. Used for Weighted Voting Games.
    def wvg_shap(self, game, agent_idx, q):
        warnings.filterwarnings('ignore')
        epsilon = np.exp(-10)
        mean = np.mean(game.stake_distribution)
        std = np.std(game.stake_distribution)

        T = 0
        n = game.n

        for X in range(1, n):
            a = (q - game.get_agent_stake(agent_idx)) / X
            b = (q - epsilon) / X

            T += st.norm.cdf((b - mean)/std) - st.norm.cdf((a - mean)/std)
        
        return T / n