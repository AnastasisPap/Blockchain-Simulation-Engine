import argparse

def get_args():
    parser = argparse.ArgumentParser(description='initialize parameters')
    parser.add_argument('--n', nargs='?', type=int, default=1000, help='The number of agents. Default is 1000.')
    parser.add_argument('--h0', nargs='?', type=int, default=32, help='The threshold to calculate the value of a stake set S.')
    parser.add_argument('--stake_distr', nargs='?', type=str, default='uniform',
                        help= 'The distribution that will be used to generate the stake for each agent.'
                        'The available distributions is the Uniform distribution.')
    parser.add_argument('--func', nargs='?', type=int, choices=range(3), default=1,
                        help='The method that will be used to calculate the agent value. 0: Shapley value - exact calculation, 1: Monte Carlo Shapley value, 2: Weighted Voting Game Shapley Value')
    parser.add_argument('--max_stake_prop', nargs='?', type=float, default=0.75, help='The proportion of the threshold that will be the maximum stake. For example if it\'s 0.75, then 0.75*threshold will be the maximum possible stake.')
    parser.add_argument('--epochs', nargs='?', type=int, default=100000, help='The maximum number of epochs for the simulation to run, if no convergence has happened.')
    parser.add_argument('--seed', nargs='?', type=int, default=10, help='The random seed')
    parser.add_argument('--m', nargs='?', type=int, default=100, help='The number of samples when using the Monte Carlo approximation for Shapley Value.')
    parser.add_argument('--a0', nargs='?', type=float, default=1.2, help='The shape of the Pareto distribution.')
    args = parser.parse_args()

    return args