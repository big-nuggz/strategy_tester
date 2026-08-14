import matplotlib.pyplot as plt

import pandas as pd

from constants import PATH_SP500


# python -m chart
if __name__ == '__main__':
    data = pd.read_csv(PATH_SP500)
    data['Date'] = pd.to_datetime(data['Date'], utc=True)
    data = data.set_index('Date')

    monthly = data.resample('ME').agg({
        'Open': 'first', 
        'High': 'max', 
        'Low': 'min', 
        'Close': 'last', 
        'Volume': 'sum'
    })

    plt.plot(monthly['Close'])
    plt.show()