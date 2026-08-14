from os.path import split as path_split
from os.path import exists as path_exists
from os import makedirs

import yfinance as yf

from constants import PATH_SP500


def download_us(path=PATH_SP500, force=False, verbose=True):
    if path_exists(path):
        if verbose: print(f'{path} already exists')
        if force:
            if verbose: print('downloading anyway...')
        else:
            return
    else:
        if verbose: print('downloading...')

    # download daily, since monthly only starts from 1985
    ticker = yf.Ticker('^GSPC')
    data = ticker.history(period='max', interval='1d')

    head, tail = path_split(path)
    makedirs(head, exist_ok=True)

    data.to_csv(path)
    if verbose: print(f'saved to {path}')


# python -m download
if __name__ == '__main__':
    download_us()