# Blockchain-Simulation-Engine

### Bin Cover
Since opening a new pool isn't currently a possible strategy, it's important for the initial assignment to have as many pools as possible (that are above the threshold). This problem is called ["Bin Cover"](https://en.wikipedia.org/wiki/Bin_covering_problem), and has an easy O(nlogn) 2/3-approximation. The algorithm that follows is from Csirik, Frenk, Lebbe, and Zhang[^1]:
> Order by decreasing order
> Fill a bin with the largest m items, such that the total stake is less than the threshold and adding the (m+1)-st largest item will result to a total stake >= threshold
> Fill the bin with the smallest items until the total stake >= threshold
> Repeat

### Reward Functions
To find the next best response of an agent we use a reward function, the main one is the Shapley Value. For each coalition that forms a pool, use the Shapley value to calculate the value of the agent by moving to that pool and choose the one which results to the highest value. Since it takes exponentially long to calculate the Shapley value, we use approximations. Two approximations are used:
- **Monte Carlo approximation**: sample permuations.
- **Weighted Voting Game approximation**: approximation created for weighted voting games (linear time without sampling) gotten from [^2].

### Simulation
1. The first phase is to initialize the agents and their actions. In this stage we use the approximation to the bin cover problem to initialize the actions of each agent.
2. We use the shapley value as described before to find the next best action for each agent.
3. If for all agents their actions didn't change, we have reached an equilibrium.
4. If no equilibrium is reached the simulation ends in two ways: (1) max epochs are reached, (2) state cycle is detected in which the current state (the actions of each agent) has been seen before. This would eventually reach max epochs.

### Argument list
- **n**: the number of agents (default=1000).
- **h0**: the threshold value for the weighted voting game (default=32).
- **stake_distr**: the distribution from which agent stakes will be sampled from. Current options are the uniform and pareto distributions (default=uniform).
- **func**: the reward function that will be used. Current options include the exact Shapley (0) and Monte Carlo shapley approximation (1).
- **max_stake_prop**: a number in (0, 1) which indicates what percentage of the threshold value will be the maximum possible stake value (default=0.75).
- **epochs**: max number of iterations (default=100000).
- **seed**: the random seed for numpy.
- **m**: the total number of samples to be taken when using the Monte Carlo approximation (default=100).
- **a0**: the shape of the pareto distribution (default=1.2).

### Running the simulation
1. From the CLI, set the arguments and run main.py, for example:
```
python main.py --n 100 --h0 50 --func 0
```
2. For VSCode, use `launch.json` and debug. For more details use the [VSCode docs](https://code.visualstudio.com/docs/python/debugging#_initialize-configurations). Example configuration for `launch.json`:
```json
{
    "name": "Debug Config={n:15, h0:15, Uniform, Exact Shapley}",
    "type": "debugpy",
    "request": "launch",
    "program": "${file}",
    "console": "integratedTerminal",
    "args": ["--n", "15", "--h0", "15", "--stake_distr", "uniform", "--func", "0"]
}
```

### Running tests
To run a specific test (named test_name.py), run the following command:
```
python -m test.test_name
```

To run all tests:
```
python -m unittest
```

### Task list (by priority)
- [ ] Implement the Weighted Voting Game Shapley approximation
- [ ] Handle hanging agents (happens when a pool owner changes strategy)
- [ ] Use multiple threads
- [ ] Handle simulation end (show graphs, store results, etc.)
- [ ] Create "whale" distribution

### Sources
[^1]: Csirik, Frenk, Lebbe, Zhang (1999). ["Two simple algorithms for bin covering"](https://cyber.bibl.u-szeged.hu/index.php/actcybern/article/view/3507)
[^2]: Fatima, Wooldridge, Jennings (2008). ["A linear approximation method for the Shapley Value"](https://doi.org/10.1016/j.artint.2008.05.003)