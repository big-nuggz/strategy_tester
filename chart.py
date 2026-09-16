import matplotlib.pyplot as plt

def save_parameter_sweep_heatmap(
        returns, 
        param_1,
        param_2, 
        title, 
        label, 
        param_1_description, 
        param_2_description, 
        path):
    Z = returns.reshape(len(param_1), len(param_2)).T
    fig, ax = plt.subplots()

    cax = ax.imshow(
        Z * 100, 
        cmap='viridis',
        origin='lower',
        extent=[param_1[0] * 100, param_1[-1] * 100, param_2[0] * 100, param_2[-1] * 100],
        aspect='auto'
    )

    fig.colorbar(cax, label=label)
    ax.set_xlabel(param_1_description)
    ax.set_ylabel(param_2_description)
    ax.set_title(title)

    ax.set_xticks(param_1 * 100)
    ax.set_yticks(param_2 * 100)

    plt.tight_layout()
    plt.savefig(path)


# python -m chart
if __name__ == '__main__':
    from data import load_sp500
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