from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta

import pandas as pd

from constants import PATH_SP500, TESTING_PERIOD


def load_sp500(path=PATH_SP500):
    data = pd.read_csv(PATH_SP500)
    data['Date'] = pd.to_datetime(data['Date'], utc=True)
    data = data.set_index('Date')

    return data

def get_slices(data, year_start, year_end):
    slices = []
    for year in range(year_start, year_end + 1):
        starting_date = datetime(year=year, month=1, day=1, tzinfo=UTC)
        end_date = starting_date + relativedelta(years=TESTING_PERIOD)
        slices += [data.loc[starting_date: end_date]]

    return slices
