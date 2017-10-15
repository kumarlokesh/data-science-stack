"""
Calculate Bollinger bands.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def get_file_path(label):
    return os.path.join("data", "{0}.csv".format(label))


def normalize_data(df):
    return df/df.ix[0,:]

def get_stock_data(labels, dates):
    df = pd.DataFrame(index=dates)

    if 'SPY' not in labels:
        labels.insert(0, 'SPY')

    for label in labels:
        # Select only Date and Adjusted Close columns from csv
        df_temp = pd.read_csv(get_file_path(label), index_col='Date',
            parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': label})
        df = df.join(df_temp)

        if label == 'SPY':
            df = df.dropna(subset=["SPY"])

    return normalize_data(df)


def plot_data(df, columns, start_index, end_index, title):
    df = df.ix[start_index:end_index, columns]
    ax = df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Prices")
    plt.show()


def get_rolling_mean(values, window):
    return values.rolling(window=window,center=False).mean()


def get_rolling_std(values, window):
    return values.rolling(window=window,center=False).std()


def get_bollinger_bands(rm, rstd):
    return (rm + (rstd*2)), (rm - (rstd*2))


def main():
    dates = pd.date_range('2010-01-01', '2010-12-31')
    stock_symbols = ['GOOG', 'IBM', 'GLD']
    df = get_stock_data(stock_symbols, dates)
    # plot_data(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01', "Stock prices")

     # Compute Bollinger Bands
    # 1. Compute rolling mean
    rm_SPY = get_rolling_mean(df['SPY'], window=20)

    # 2. Compute rolling standard deviation
    rstd_SPY = get_rolling_std(df['SPY'], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)

    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
    rm_SPY.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Prices")
    ax.legend(loc='upper left')
    plt.show()


if __name__ == "__main__":
    main()