# Blockchain-Simulation-Engine

### Bin Cover
Since opening a new pool isn't currently a possible strategy, it's important for the initial assignment to have as many pools as possible (that are above the threshold). This problem is called ["Bin Cover"](https://en.wikipedia.org/wiki/Bin_covering_problem), and has an easy O(nlogn) 2/3-approximation. The algorithm that follows is from Csirik, Frenk, Lebbe, and Zhang[^1]:
> Order by decreasing order<br/>
> Fill a bin with the largest m items, such that the total stake is less than the threshold and adding the (m+1)-st largest item will result to a total stake >= threshold<br/>
> Fill the bin with the smallest items until the total stake >= threshold<br/>
> Repeat

### Reward Functions
To find the next best response of an agent we use a reward function, the main one is the Shapley Value. For each coalition that forms a pool, use the Shapley value to calculate the value of the agent by moving to that pool and choose the one which results to the highest value. We calculate the Shapley value using two functions:
- **Exact algorithm**: finds the Shapley value exactly. Takes **exponential** time!
- **Weighted Voting Game approximation**: approximation created for weighted voting games (linear time without sampling) gotten from [^2].

### Simulation
1. The first phase is to initialize the agents and their actions. In this stage we use the approximation to the bin cover problem to initialize the actions of each agent.
2. We use the shapley value as described before to find the next best action for each agent.
3. If for all agents their actions didn't change, we have reached an equilibrium.
4. If no equilibrium is reached the simulation ends in two ways: (1) max epochs are reached, (2) state cycle is detected in which the current state (the actions of each agent) has been seen before. This would eventually reach max epochs.

### Create the config file
Each configuration file **must** include all of the following. If an argument can take multiple values, it **must always** be used as a list.
To avoid possible errors, you can use the config.json file from this repo and change/add values.

- **n (list[int])**: the number of agents.
- **max_stake (list[int])**: the max stake any agent can have. A whale will have stake equal to this.
- **stake_distr ("uniform" | "whale" | "pareto")**: the distribution from which agent stakes will be sampled from. Current options are the uniform, whale, and pareto distributions.
- **func (0 | 1)**: the reward function that will be used. Current options include the exact Shapley (0) and from [^2] the Weighted Voting Game Approximation (1).
- **exp_pools (list[int])**: the number of expected pools.
- **epochs (int)**: max number of iterations.
- **seed (int)**: the random seed for numpy.
- **a0 (float)**: the shape of the pareto distribution.
- **max_workers (int)**: the number of workers to be used/number of parallel pools to be created.
- **execution_id (str)**: the name for this execution. This will be used as the file name for the output.
- **iterations (int)**: number of iterations to perform for each configuration. The average of all iterations is taken.

### Calculation of the threshold value h
```math
\frac{\sum^n\mathbb{E}[s_i]}{h}=\frac{n}{k}
```
Where $s_i$=stake of agent $i$ and $\frac{n}{k}$ is the number of expected pools.

### Running the simulation
1. From the CLI, set the arguments and run main.py, for example:
```
python main.py ./path/to/config.json
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

### Interpreting results
In the results folder, the results are stored in folders based on their execution id (set in config file). Each of these folders has:
 - Graphs: the graphs store all the heatmap combinations of the batch parameters. The name of each file is the parameter that is kept constant and its value.
 - data: stores unprocessed data of each simulation, including values set used by the config file, agent information (ID, action, stake), # of pools created, # of iterations until convergence.
 - results: holds aggregated information (average by number of iterations), similar to data but more processed.

### Task list (by priority)
- [ ] Code cleanup

[^1]: Csirik, Frenk, Lebbe, Zhang (1999). ["Two simple algorithms for bin covering"](https://cyber.bibl.u-szeged.hu/index.php/actcybern/article/view/3507)
[^2]: Fatima, Wooldridge, Jennings (2008). ["A linear approximation method for the Shapley Value"](https://doi.org/10.1016/j.artint.2008.05.003)
