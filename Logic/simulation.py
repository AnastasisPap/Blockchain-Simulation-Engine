from tqdm.notebook import tqdm
import time
import numpy as np
from Logic.agent import Agent
from Logic.bin_cover import bin_cover_approx
from Logic.reward_functions import RewardFunctions

# TODO(anastasis): use multiple threads
class Simulation:
    # Agent action at index i:
    #   i -> the player with ID=i owns the pool
    #   j -> the player with ID=i is has a stake in the pool of agent with ID=j
    def __init__(self, args):
        self.n = args.n
        self.h0 = args.h0
        self.a0 = args.a0
        self.stake_distr = args.stake_distr.lower()
        extra_args = [args.m] if args.m else []
        self.reward_function = RewardFunctions(args.func, extra_args)
        self.max_stake_prop = args.max_stake_prop
        self.agents = []
        self.agent_actions = np.zeros(self.n)
        self.seed = args.seed if args.seed else None
        self.max_epochs = args.epochs
        self.agent_stakes = []
        self.previous_states = set([]) # used to check if there are cycles of states (which will eventually reach max epochs)
        self.initial_num_of_pools = 0

    def start(self):
        self.initialize_agents()
        self.agents, self.initial_num_of_pools = bin_cover_approx(self.agents)
        self.agent_actions = np.array([agent.pool for agent in self.agents])

        sim_timer_start = time.perf_counter()
        for iter in tqdm(range(self.max_epochs + 1)):
            converged = self.step()

            if converged:
                self.finish_simulation(iter, True)
                return

            curr_state = str([agent.pool for agent in self.agents])
            if curr_state in self.previous_states:
                self.finish_simulation(iter)
                return
            else: self.previous_states.add(curr_state)

        if iter == self.max_epochs:
            sim_timer_end = time.perf_counter()
            print(f'Simulation finished after {sim_timer_end - sim_timer_start:0.2f} seconds.')
            self.finish_simulation(iter)
            return
    
    def finish_simulation(self, iter, converged=False):
        opt_ub = int(np.ceil(sum([agent.stake for agent in self.agents])/self.n))
        final_agent_actions = np.array([agent.pool for agent in self.agents])
        total_pools = len(np.where(final_agent_actions == np.arange(self.n))[0])

        if converged: print(f'Simulation converged after {iter + 1} iterations. Initially there were {self.initial_num_of_pools} pools and converged to {total_pools} pools. The upper bound for the optimal number of pools is {opt_ub}.')
        elif iter < self.max_epochs: print(f'Cycle detected without reaching equilibrium.')
        else: print(f'Simulation did not converge to an equilibrium (max epochs reached).')
        # TODO(anastasis): show graphs

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

    # TODO(anastasis): Create the "whale" stake distribution
    def initialize_agents(self):
        stakes = np.array([])
        if self.seed:
            np.random.seed(self.seed)

        if self.stake_distr == 'uniform':
            stakes = np.random.randint(1, self.h0 * self.max_stake_prop, self.n)
        elif self.stake_distr == 'pareto':
            max_stake = int(self.h0 * self.max_stake_prop)
            stakes = np.ceil(np.random.pareto(np.random.pareto(self.a0, self.n))).astype(int)
            stakes[np.where(stakes > max_stake)[0]] = max_stake

        for i in range(self.n):
            self.agents.append(Agent(i, stakes[i], self.h0, self.reward_function))
        
        self.agent_stakes = stakes