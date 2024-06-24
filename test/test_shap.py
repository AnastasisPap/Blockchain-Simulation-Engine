import unittest
from Logic.reward_functions import *
from Logic.game import Game
from Logic.agent import Agent

class TestExactShapley(unittest.TestCase):
    def test_5_agents(self):
        stake_distribution = np.array([1, 2, 3, 2, 1])
        threshold = 6
        agents = []
        for i in range(len(stake_distribution)):
            agents.append(Agent(i, stake_distribution[i], threshold, None))

        game = Game(agents)
        actual_sv = 11/30

        exact_shap_func = RewardFunctions(0)
        res = exact_shap_func.get_value(game, 2)
        self.assertAlmostEqual(res, actual_sv, 5)

if __name__ == '__main__':
    unittest.main()