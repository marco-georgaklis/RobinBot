"""
This file creates a sklearn linear regression model for predicting
the price change of stock of companies that design and manufacture
CPUs using the prior day's price change in cryptocurrencies
"""
import config
import robin_stocks as rb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

username = config.robinUser
password = config.robinPassword

# login to robinhood
rb.login(username, password)


def shift_string(date):
    """
    :param date: the date of the respective stock price
     change in the pandas dataframe
    :return: the date shifted back one day to line up with
    the prior days crypto price change
    the predictors
    """
    s = str(int(date[8:10]) - 1)
    if len(s) == 1:
        s = '0' + s
    return date[:8] + s + date[10:]


def shift_day_up_1(df):
    """
    :param df: the dataframe for which the date shift
    needs to occur
    :return: the dataframe with the date column shifted
    """
    return df['begins_at'].apply(shift_string)


def set_dataframe_index(df):
    """
    function sets index to the date column
    """
    df.set_index('begins_at', inplace=True)


def set_prices_to_floats(df):
    """
    :param df: the stock price dataframe
    :return: the dataframe with the opening and closing prices
    represented as floats instead of strings and a new column
    added for percent change over that day
    """
    df['open_price'] = df['open_price'].astype(float)
    df['close_price'] = df['close_price'].astype(float)
    df['pct_change'] = (df['close_price'] - df['open_price']) / df['open_price']


def prepare_data(dfList):
    """
    takes every dataframe in dfList and prepares it for the data merge
    """
    for df in dfList:
        set_dataframe_index(df)
        set_prices_to_floats(df)
        drop_bad_columns(df)


def drop_bad_columns(df):
    df.drop(["open_price", 'close_price', 'high_price', 'low_price', 'volume', 'session',
             'interpolated', 'symbol'], axis=1, inplace=True)


def avg_pct_change(df):
    df['avg_change'] = (df['pct_change_a'] + df['pct_change_b']) / 2
    df.drop(['pct_change_a', 'pct_change_b'], axis=1, inplace=True)


# use robin_stocks to acquire historical data from stock data robinhood
amd = pd.DataFrame(rb.stocks.get_stock_historicals('AMD', interval='day', span='5year'))
intel = pd.DataFrame(rb.stocks.get_stock_historicals('INTC', interval='day', span='5year'))
btc = pd.DataFrame(rb.crypto.get_crypto_historicals('BTC', interval='day', span='5year'))
eth = pd.DataFrame(rb.crypto.get_crypto_historicals('ETH', interval='day', span='5year'))
df_list = [amd, intel, btc, eth]

amd['begins_at'] = shift_day_up_1(amd)
intel['begins_at'] = shift_day_up_1(intel)

prepare_data()

merger_stocks = pd.merge(amd, intel, on='begins_at', how='outer', suffixes=('_a', '_b'))
merger_crypto = pd.merge(btc, eth, on='begins_at', how='outer', suffixes=('_a', '_b'))

avg_pct_change(merger_stocks)
avg_pct_change(merger_crypto)

total_merge = pd.merge(merger_crypto, merger_stocks, on='begins_at', how='outer',
                       suffixes=('_a', '_b'))

total_merge.dropna(inplace=True)
total_merge = total_merge[total_merge['avg_change_a'] != 0]

# Linear Regression


x_train, x_test, y_train, y_test = train_test_split(pd.DataFrame(total_merge['avg_change_a']),
                                                    total_merge['avg_change_b'], test_size=0.33)

lmo = LinearRegression()
lmo.fit(x_train, y_train)
predictions = lmo.predict(x_test)
trial = pd.DataFrame([predictions, y_test])
