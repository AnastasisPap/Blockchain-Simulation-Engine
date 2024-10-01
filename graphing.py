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
                data['n'], data['max_stake'], data['k'], 
                data['results']['avg_total_pools'], data['results']['avg_init_pools'],
                data['results']['avg_opt_ub']
            ])
        df = pd.DataFrame(rows, columns=['n', 'max_stake', 'k', 'avg_total_pools', 'avg_init_pools', 'avg_opt_ub'])
        self.data = df
    
    def generate_heatmaps(self):
        """For each entry in the list of DataFrames, it calculates the ratio of the total pools to the initial pools
        and the total pools to the optimal upper bound. Then it creates a heatmap for each of these ratios.
        """
        dfs, names = self.create_pair_dfs()

        heatmaps_init = []
        heatmaps_opt = []

        for i in range(len(dfs)):
            params = list(set(dfs[i].columns)-set(self.metrics))
            dfs[i]['total_vs_init_pools'] = dfs[i]['avg_total_pools'] / dfs[i]['avg_init_pools']
            dfs[i]['total_vs_opt_pools'] = dfs[i]['avg_total_pools'] / dfs[i]['avg_opt_ub']

            heatmaps_opt.append(dfs[i].pivot(columns=params[0], index=params[1], values='total_vs_opt_pools'))
            heatmaps_init.append(dfs[i].pivot(columns=params[0], index=params[1], values='total_vs_init_pools'))
        
        return heatmaps_opt, heatmaps_init, names
    
    def create_pair_dfs(self):
        params = ['n', 'max_stake', 'k']
        col_names = set(self.data.columns)

        dfs = []
        names = []

        for param in params:
            curr_cols = list(col_names - set([param]))

            gb = self.data.groupby(param)
            dfs += [v[curr_cols] for k, v in gb]
            curr_keys = [k for k, v in gb]
            names += [f'{param}={k}' for k in curr_keys]
        
        return dfs, names

    
    def store_heatmaps(self, path):
        """Store the heatmaps in the specified path
        """
        heatmaps_opt, heatmaps_init, names = self.generate_heatmaps()

        if not os.path.exists(path):
            os.makedirs(path)

        for i in range(len(names)):
            plt.title(f'Total Pools vs Optimal Upper Bound ({names[i]})')
            sns.heatmap(heatmaps_opt[i], annot=True, vmin=0, vmax=1)
            plt.savefig(f'{path}/{names[i]}_opt.png')
            plt.close()

            plt.title(f'Total Pools vs Initial Pools ({names[i]})')
            sns.heatmap(heatmaps_init[i], annot=True, vmin=0, vmax=1)
            plt.savefig(f'{path}/{names[i]}_init.png')
            plt.close()