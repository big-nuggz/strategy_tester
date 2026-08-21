import pandas as pd

from constants import PATH_SP500


def load_sp500(path=PATH_SP500):
    data = pd.read_csv(PATH_SP500)
    data['Date'] = pd.to_datetime(data['Date'], utc=True)
    data = data.set_index('Date')

    return data