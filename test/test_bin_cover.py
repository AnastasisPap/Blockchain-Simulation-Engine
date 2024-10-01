import unittest
from Logic.bin_cover import bin_cover_approx
from Logic.agent import Agent

class TestBinCover(unittest.TestCase):
    def test_end_in_max_ptr(self):
        threshold = 1
        stakes = [0.5, 0.6, 0.2, 0.2, 0.1, 0.9, 0.3, 0.6, 0.3]
        exp_pools = [0, 1, 1, 1, 5, 5, 7, 7, 7]

        agents = []
        for i in range(len(stakes)):
            agents.append(Agent(i, stakes[i], threshold, None))

        agents = bin_cover_approx(agents)
        for agent in agents:
            self.assertEqual(exp_pools[agent.id], agent.pool)

    def test_end_in_min_ptr(self):
        threshold = 1
        stakes = [0.5, 0.6, 0.2, 0.2, 0.1, 0.9, 0.3, 0.6, 0.3, 0.4]
        exp_pools = [0, 1, 1, 1, 5, 5, 7, 7, 7, 0]

        agents = []
        for i in range(len(stakes)):
            agents.append(Agent(i, stakes[i], threshold, None))

        agents = bin_cover_approx(agents)
        for agent in agents:
            self.assertEqual(exp_pools[agent.id], agent.pool)

if __name__ == '__main__':
    unittest.main()