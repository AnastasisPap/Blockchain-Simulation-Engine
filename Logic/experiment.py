import multiprocessing as mp
from Logic.simulation import Simulation
import time

class Experiment:
    def __init__(self, args, configurations):
        """
        Args:
         - args(dict): arguments in the same format as in the config.json file
         - configurations(list): list of dictionaries with the configurations to run the experiment.
            The configurations are made from args but do not have multiple values for some argument.
        """
        self.args = args
        self.configurations = configurations
    
    def run(self):
        start_time = time.time()
        outputs = {}

        pool = mp.Pool(processes=self.args.get('max_workers'))
        num_of_iterations = self.args.get('iterations')

        simulations = [Simulation(config) for config in self.configurations for _ in range(num_of_iterations)]
        results = [pool.apply_async(sim.start) for sim in simulations]
        # Wait for all the processes to finish to avoid race conditions when writing to the outputs dictionary
        [pool.wait() for pool in results]
        
        for res in results:
            output = res.get()
            config_id = output.get('config_id')

            if config_id not in outputs: outputs[config_id] = []
            outputs[config_id].append(output)

        end_time = time.time()
        print(f'Experiment finished after {int(end_time - start_time)} seconds.')

        return outputs