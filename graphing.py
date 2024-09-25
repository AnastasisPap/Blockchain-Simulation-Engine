import itertools
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Graphing:
    def __init__(self, data):
        """
        Args:
         - data(dict): dictionary with the processed data from the handle outputs function
        """
        self.data = data
        self.metrics = ['avg_total_pools', 'avg_init_pools', 'avg_opt_ub']
        self.convert_data_to_df()
    
    def convert_data_to_df(self):
        """Converts the data dictionary to a pandas DataFrame for easier processing 
        """
        rows = []

        for config_id, data in self.data.items():
            rows.append([
                data['n'], data['h0'], data['a0'], data['max_stake_prop'],
                data['results']['avg_total_pools'], data['results']['avg_init_pools'],
                data['results']['avg_opt_ub']
            ])
        df = pd.DataFrame(rows, columns=['n', 'h0', 'a0', 'max_stake_prop', 'avg_total_pools', 'avg_init_pools', 'avg_opt_ub'])
        self.data = df
    
    def create_pair_dfs(self):
        """Finds all possible combinations of pairs of parameters and creates a DataFrame for each pair
        by grouping the data by that pair. Also stores the name of each DataFrame (which is the grouping parameters).
        This creates a list 2-D grid of values which will be used to create heatmaps.
        """
        col_names = set(self.data.columns)
        params = ['n', 'h0', 'a0', 'max_stake_prop']
        pairs = list(itertools.combinations(params, 2))

        dfs = []
        names = []

        for pair in pairs:
            # curr_cols = all the initial columns without the columns which are used to group by
            curr_cols = list(col_names-set(pair))

            gb = self.data.groupby(list(pair))
            dfs += [v[curr_cols] for k, v in gb]
            curr_keys = [k for k, v in gb]
            names += [f'{pair[0]}_{k[0]}_{pair[1]}_{k[1]}' for k in curr_keys]
        
        return dfs, names
    
    def generate_heatmaps(self):
        """For each entry in the list of DataFrames, it calculates the ratio of the total pools to the initial pools
        and the total pools to the optimal upper bound. Then it creates a heatmap for each of these ratios.
        """
        dfs, names = self.create_pair_dfs()

        heatmaps_opt = []
        heatmaps_init = []

        for i in range(len(dfs)):
            dfs[i]['total_vs_init_pools'] = dfs[i]['avg_total_pools'] / dfs[i]['avg_init_pools']
            dfs[i]['total_vs_opt_pools'] = dfs[i]['avg_total_pools'] / dfs[i]['avg_opt_ub']
            # Dimensoins are the two dimensions which will be the axis of the heatmap
            dimensions = list(set(dfs[i].columns) - {'avg_total_pools', 'avg_init_pools', 'avg_opt_ub', 'total_vs_init_pools', 'total_vs_opt_pools'})

            heatmaps_opt.append(dfs[i].pivot(columns=dimensions[0], index=dimensions[1], values='total_vs_opt_pools'))
            heatmaps_init.append(dfs[i].pivot(columns=dimensions[0], index=dimensions[1], values='total_vs_init_pools'))
        
        return heatmaps_opt, heatmaps_init, names
    
    def store_heatmaps(self, path):
        """Store the heatmaps in the specified path
        """
        heatmaps_opt, heatmaps_init, names = self.generate_heatmaps()

        if not os.path.exists(path):
            os.makedirs(path)

        for i in range(len(heatmaps_opt)):
            sns.heatmap(heatmaps_opt[i], annot=True, vmin=0, vmax=1)
            plt.savefig(f'{path}/{names[i]}_opt.png')
            plt.close()

            sns.heatmap(heatmaps_init[i], annot=True, vmin=0, vmax=1)
            plt.savefig(f'{path}/{names[i]}_init.png')
            plt.close()