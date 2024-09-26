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
                data['n'], data['max_stake'], data['a0'], 
                data['results']['avg_total_pools'], data['results']['avg_init_pools'],
                data['results']['avg_opt_ub']
            ])
        df = pd.DataFrame(rows, columns=['n', 'max_stake', 'a0', 'avg_total_pools', 'avg_init_pools', 'avg_opt_ub'])
        self.data = df
    
    def generate_heatmaps(self):
        """For each entry in the list of DataFrames, it calculates the ratio of the total pools to the initial pools
        and the total pools to the optimal upper bound. Then it creates a heatmap for each of these ratios.
        """
        df = self.data[['n', 'max_stake', 'avg_total_pools', 'avg_init_pools', 'avg_opt_ub']]
        df['total_vs_init_pools'] = df['avg_total_pools'] / df['avg_init_pools']
        df['total_vs_opt_pools'] = df['avg_total_pools'] / df['avg_opt_ub']

        heatmap_opt = df.pivot(columns='n', index='max_stake', values='total_vs_opt_pools')
        heatmap_init = df.pivot(columns='n', index='max_stake', values='total_vs_init_pools')
        
        return heatmap_opt, heatmap_init
    
    def store_heatmaps(self, path):
        """Store the heatmaps in the specified path
        """
        heatmap_opt, heatmap_init = self.generate_heatmaps()

        if not os.path.exists(path):
            os.makedirs(path)

        plt.title(f'Total Pools vs Optimal Upper Bound')
        sns.heatmap(heatmap_opt, annot=True, vmin=0, vmax=1)
        plt.savefig(f'{path}/n_max_stake_opt.png')
        plt.close()

        plt.title(f'Total Pools vs Initial Pools')
        sns.heatmap(heatmap_init, annot=True, vmin=0, vmax=1)
        plt.savefig(f'{path}/n_max_stake_init.png')
        plt.close()