import numpy as np
from datetime import datetime

from markdown import generate_table, get_best_indices


def print_result(results: list, period: int, prefix=None) -> None:
    if prefix:
        print(prefix)

    mean_return, low, high, std, cagr = get_result_metrics(results, period)

    print(f'mean return: {mean_return * 100:.2f}%, mean CAGR: {cagr * 100:.2f}%')
    print(f'low: {low * 100:.2f}%, high: {high * 100:.2f}%, std: {std * 100:.2f}%')

    return

def get_result_metrics(results: list, period: int):
    mean_return = np.mean(results)
    low = np.min(results)
    high = np.max(results)
    std = np.std(results)
    cagr = (mean_return + 1) ** (1 / period) - 1

    return (mean_return, low, high, std, cagr)

def generate_report(
        path: str, 
        results_price_only: list, 
        results_total_return: list, 
        period: int, 
        prefixes: list, 
        date: datetime):
    """
    generates and writes a neat markdown result
    """
    date_text = date.isoformat()
    
    # table headers
    header = ['Strategy', 'Mean 10 Year Return', 'Minimum 10 Year Return', 'Maximum 10 Year Return', 'Std. Deviation', 'Mean CAGR']

    units = ['', '%', '%', '%', '%', '%']
    evaluators=[None, np.argmax, np.argmax, np.argmax, np.argmin, np.argmax]

    data_price_only = [header]
    for result, prefix in zip(results_price_only, prefixes):
        mean_return, low, high, std, cagr = get_result_metrics(result, period)
        data_price_only += [[
            prefix, 
            float(mean_return * 100), 
            float(low * 100), 
            float(high * 100), 
            float(std * 100), 
            float(cagr * 100)]]

    data_total_return = [header]
    for result, prefix in zip(results_total_return, prefixes):
        mean_return, low, high, std, cagr = get_result_metrics(result, period)
        data_total_return += [[
            prefix, 
            float(mean_return * 100), 
            float(low * 100), 
            float(high * 100), 
            float(std * 100), 
            float(cagr * 100)]]

    table_price_only = generate_table(
        data_price_only, 
        units=units, 
        highlights=get_best_indices(data_price_only, evaluators))

    table_total_return = generate_table(
        data_total_return, 
        units=units, 
        highlights=get_best_indices(data_total_return, evaluators))

    with open(path, 'w', encoding='utf8') as f:
        f.write(f'# Test Result Report (run: {date_text})')
        f.write('\n' * 2)
        f.write(f'## S&P 500 Price Only')
        f.write('\n' * 2)
        f.write(table_price_only)
        f.write('\n' * 2)
        f.write(f'## S&P 500 Total Return')
        f.write('\n' * 2)
        f.write(table_total_return)
        f.write('\n')