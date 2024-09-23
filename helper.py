import itertools

def generate_configs(args):
    """
    Args:
     - args(dict): dictionary with the arguments in the same format as in the config.json file
    
    Returns:
     - args_list(list): list of dictionaries with the configurations to run the experiment.
    """
    list_n = args.get('n')
    list_h0 = args.get('h0')
    list_max_stake = args.get('max_stake_prop')
    list_a0 = args.get('a0')

    # Generate all possible combinations of the arguments
    configurations = itertools.product(list_n, list_h0, list_max_stake, list_a0)

    args_list = []
    for i, config in enumerate(configurations):
        n, h0, max_stake, a0 = config
        args['n'] = n
        args['h0'] = h0
        args['max_stake_prop'] = max_stake
        args['a0'] = a0
        args['config_id'] = f'config_{i+1}'
        args_list.append(args.copy())
    
    return args_list

def handle_outputs(outputs):
    """Finds the average of some metrics across iterations for the same configurations

    Args:
     - outputs(dict): dictionary with the outputs from the
    
    Returns:
     - processed_out(dict): dictionary with the processed outputs
    """
    processed_out = {}

    for config_id, data in outputs.items():
        total_pools = 0
        init_pools = 0
        opt_ub = 0

        for item in data:
            total_pools += item['total_pools']
            init_pools += item['initial_num_of_pools']
            opt_ub += item['opt_ub']
    
        total_pools /= len(data)
        init_pools /= len(data)
        opt_ub /= len(data)
        processed_out[config_id] = {
            'avg_total_pools': total_pools,
            'avg_init_pools': init_pools,
            'avg_opt_ub': opt_ub
        }
    
    return processed_out