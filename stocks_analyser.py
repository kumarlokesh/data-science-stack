"""
Script to read stocks information from csv files.
Capability to slice and plot data using pandas and
matplotlib.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def get_file_path(label):
    return os.path.join("data", "{0}.csv".format(label))


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

    return df


def plot_data(df, columns, start_index, end_index, title):
    df = df.ix[start_index:end_index, columns]
    ax = df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Prices")
    plt.show()


def main():
    dates = pd.date_range('2010-01-01', '2010-12-31')
    stock_symbols = ['GOOG', 'IBM', 'GLD']
    df = get_stock_data(stock_symbols, dates)
    plot_data(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01', "Stock prices")


if __name__ == "__main__":
    main()