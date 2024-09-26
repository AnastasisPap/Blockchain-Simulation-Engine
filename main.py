import sys
import json
from Logic.experiment import Experiment
from helper import generate_configs, handle_outputs
from graphing import Graphing

def main():
    config_file_path = sys.argv[1]
    with open(config_file_path, 'r') as f:
        args = json.load(f)
    configs = generate_configs(args.copy())

    # Run experiment. The difference between an experiment and a simulation
    # is that the experiment runs multiple simulations with different configurations
    experiment = Experiment(args, configs)
    data = experiment.run()

    processed_data = handle_outputs(data)

    graph = Graphing(processed_data)
    graph.store_heatmaps(f'./results/{args.get("execution_id")}/graphs')

    results_file = f'./results/{args.get("execution_id")}/results.json'
    with open(results_file, 'w') as f:
        json.dump(processed_data, f)
    

if __name__ == '__main__':
    main()