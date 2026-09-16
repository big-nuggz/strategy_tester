from os.path import join as path_join

import numpy as np

from constants import *
from data import load_sp500, get_slices
from chart import save_parameter_sweep_heatmap
from test import run_test
from results import print_result
from strategy.reverse_timed_dca import ReverseTimedDCA


if __name__ == '__main__':
    # generate parameter grid for the timed dca
    param_dca_portion = np.linspace(0.2, 0.8, 7)
    param_threshold = np.linspace(0.95, 0.99, 5)
    param_grid = [(round(dca_portion, 2), round(threshold, 2)) for dca_portion in param_dca_portion for threshold in param_threshold]

    strategies = [ReverseTimedDCA for _ in range(len(param_grid))]
    
    parameters = [
        {'budget': BUDGET, 'years': 5, 'dca_portion': dca_portion, 'threshold': threshold} 
        for dca_portion, threshold in param_grid
    ]

    slices_price_only = get_slices(load_sp500(path=PATH_SP500), YEAR_START, YEAR_END)
    results_price_only = run_test(slices_price_only, strategies, parameters)

    slices_total_return = get_slices(load_sp500(path=PATH_SP500_TR), YEAR_START_TOTAL_RETURN, YEAR_END)
    results_total_return = run_test(slices_total_return, strategies, parameters)

    # show and save results
    prefixes = [strategy.name for strategy in strategies]

    print('S&P 500 price only')
    print(f'{TESTING_PERIOD} year testing period, number of samples = {len(slices_price_only)}')
    print('=' * 40)
    
    for result, prefix in zip(results_price_only, prefixes):
        print('-' * 40)
        print_result(result, TESTING_PERIOD, prefix)

    print('S&P 500 total return')
    print(f'{TESTING_PERIOD} year testing period, number of samples = {len(slices_total_return)}')
    print('=' * 40)
    
    for result, prefix in zip(results_total_return, prefixes):
        print('-' * 40)
        print_result(result, TESTING_PERIOD, prefix)

    # chart it out
    timed_dca_returns = np.mean(results_price_only, axis=1)

    save_parameter_sweep_heatmap(
        timed_dca_returns, 
        param_dca_portion, 
        param_threshold, 
        'Reverse Timed DCA Parameter Sweep (Price Only)', 
        'Mean 10 Year Returns (%)', 
        'Fixed Contribution Portion (%)', 
        'Market Dip Threshold (%)', 
        path_join(PATH_CHART_ROOT, 'reverse_timed_dca_parameter_sweep_PO.png'))

    timed_dca_returns = np.mean(results_total_return, axis=1)

    save_parameter_sweep_heatmap(
        timed_dca_returns, 
        param_dca_portion, 
        param_threshold, 
        'Reverse Timed DCA Parameter Sweep (Total Return)', 
        'Mean 10 Year Returns (%)', 
        'Fixed Contribution Portion (%)', 
        'Market Dip Threshold (%)', 
        path_join(PATH_CHART_ROOT, 'reverse_timed_dca_parameter_sweep_TR.png'))