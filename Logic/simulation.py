import numpy as np
import time
from Logic.agent import Agent
from Logic.bin_cover import bin_cover_approx
from Logic.reward_functions import RewardFunctions

class Simulation:
    # Agent action at index i:
    #   i -> the player with ID=i owns the pool
    #   j -> the player with ID=i is has a stake in the pool of agent with ID=j
    def __init__(self, args):
        self.data = args
        self.n = args.get('n')
        self.max_stake = args.get('max_stake')
        self.a0 = args.get('a0', None)
        self.stake_distr = args.get('stake_distr').lower()
        self.config_id = args.get('config_id')
        self.exp_pools = args.get('exp_pools')

        extra_args = []
        func = args.get('func')

        """
        In case you want to pass extra arguments to the RewardFunctions class
         replace X with the appropriate selection number and the extra arguments
        if func == X:
            extra_args = [args.h0]
        """

        self.reward_function = RewardFunctions(func, extra_args)
        self.agents = []
        self.agent_actions = np.zeros(self.n)
        self.seed = args.get('seed', None)
        self.max_epochs = args.get('epochs')
        self.agent_stakes = []
        self.previous_states = set([]) # used to check if there are cycles of states (which will eventually reach max epochs)
        self.initial_num_of_pools = 0

        self.whale_prob = args.get('whale_prob', 0.05) # Used for whale distribution

    def start(self):
        print(f'Starting configuration with id: {self.config_id}...')
        self.start_time = time.time()
        self.initialize_agents()
        self.agents, self.initial_num_of_pools = bin_cover_approx(self.agents)
        self.agent_actions = np.array([agent.pool for agent in self.agents])

        for iter in range(self.max_epochs+1):
            converged = self.step()

            if converged:
                return self.finish_simulation(iter, True)

            curr_state = str([agent.pool for agent in self.agents])
            if curr_state in self.previous_states:
                return self.finish_simulation(iter)
            else: self.previous_states.add(curr_state)

        if iter == self.max_epochs:
            print(f'Simulation reached max epochs.')
            return self.finish_simulation(iter)
    
    def finish_simulation(self, iter, converged=False):
        end_time = time.time()
        print(f'Finished configuration {self.config_id} after {int(end_time - self.start_time)} seconds.')

        opt_ub = int(np.ceil(sum([agent.stake for agent in self.agents])/self.h0))
        final_agent_actions = np.array([agent.pool for agent in self.agents])
        total_pools = len(np.where(final_agent_actions == np.arange(self.n))[0])

        res = {
            'iter': iter,
            'converged': converged,
            'initial_num_of_pools': self.initial_num_of_pools,
            'total_pools': total_pools,
            'opt_ub': opt_ub,
            'config_id': self.config_id,
        }

        self.data['results'] = res
        self.data['agents'] = [agent.to_dict() for agent in self.agents]

        return self.data

    def step(self):
        converged = True
        for agent in self.agents:
            prev_action = agent.pool
            action = agent.choose_action(self.agents)
            if prev_action != action: converged = False

            # TODO(anastasis): handle hanging agents (a pool owner decides to close the pool)
            if action > 0 and prev_action == 0:
                self.agent_actions[np.where(self.agent_actions == agent.id)] = 0
        
        return converged

    def initialize_agents(self):
        stakes = np.array([])
        if self.seed:
            np.random.seed(self.seed)

        if self.stake_distr == 'uniform':
            h0 = (1+self.max_stake) * self.n / (2*self.exp_pools)
            stakes = np.random.uniform(1, self.max_stake, self.n)
        elif self.stake_distr == 'pareto':
            h0 = (self.a0 * self.n) / ((self.a0 - 1) * self.exp_pools)
            stakes = np.random.pareto(np.random.pareto(self.a0, self.n))
            stakes[np.where(stakes > self.max_stake)[0]] = self.max_stake
        elif self.stake_distr == 'whale':
            h0 = (1-self.whale_prob + self.whale_prob * self.max_stake) * self.n / self.exp_pools
            stakes = np.random.choice(
                [1, self.max_stake],
                p=[1-self.whale_prob, self.whale_prob],
                size=self.n)
            
        self.h0 = h0
        for i in range(self.n):
            self.agents.append(Agent(i, stakes[i], self.h0, self.reward_function))
        
        self.agent_stakes = stakes