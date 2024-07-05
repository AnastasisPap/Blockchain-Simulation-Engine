import numpy as np

class Game:
    def __init__(self, agents):
        self.threshold = agents[0].threshold_value if len(agents) else 0
        self.stake_distribution = np.array([agent.stake for agent in agents])
        self.agent_ids = np.array([agent.id for agent in agents])
        self.agents = agents
        self.n = len(agents)
    
    def utility(self, agents_subset, agent_id):
        agents_subset_idxes = np.where(np.isin(self.agent_ids, agents_subset))[0]
        coalition_stake = np.sum(self.stake_distribution[agents_subset_idxes]) if len(agents_subset) > 0 else 0

        agent_idx = np.where(self.agent_ids == agent_id)[0]
        return int(((coalition_stake + self.stake_distribution[agent_idx]) >= self.threshold)) - int(coalition_stake >= self.threshold)
    
    def get_agent_ids(self):
        return set([agent.id for agent in self.agents])
    
    def get_agent_stake(self, agent_id):
        if agent_id not in self.agent_ids: raise Exception("Can't find such agent id")
        idx = np.where(self.agent_ids == agent_id)[0][0]
        return self.stake_distribution[idx]
