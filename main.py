import sys
import json
from Logic.experiment import Experiment
from helper import generate_configs, handle_outputs

def main():
    config_file_path = sys.argv[1]
    with open(config_file_path, 'r') as f:
        args = json.load(f)
    configs = generate_configs(args.copy())

    # Run experiment. The difference between an experiment and a simulation
    # is that the experiment runs multiple simulations with different configurations
    experiment = Experiment(args, configs)
    outputs = experiment.run()

    full_results = {'args': args, 'results': outputs}
    results_file = f'./results/{args.get("execution_id")}.json'
    with open(results_file, 'w') as f:
        json.dump(full_results, f)

    processed_data = handle_outputs(outputs)
    print(processed_data)

if __name__ == '__main__':
    main()