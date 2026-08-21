import matplotlib.pyplot as plt

import pandas as pd

from data import load_sp500


# python -m chart
if __name__ == '__main__':
    data = load_sp500()

    monthly = data.resample('ME').agg({
        'Open': 'first', 
        'High': 'max', 
        'Low': 'min', 
        'Close': 'last', 
        'Volume': 'sum'
    })

    plt.plot(monthly['Close'])
    plt.show()