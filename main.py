import robin_stocks as rb
import config
import twitter

# import the username and password from the config.py file. If you choose to clone this
# repository and upload online, include the config.py file in gitignore to keep your
# personal information hidden
username = config.robinUser
password = config.robinPassword

# login to robinhood
rb.login(username, password)


# practicing with the robin stocks library
def practice():
    # list all available cryptocurrencies for purchase
    print(rb.get_crypto_currency_pairs())

    # Of those cryptos, print their symbols
    for crypto in rb.get_crypto_currency_pairs():
        print(crypto['asset_currency']['code'])

    # getting historical data from a cryptocurrency, particularly the performance each day for
    # the past week
    print(rb.get_crypto_historical("BTC", 'day', 'week', '24_7'))


# This function uses Twitter and Reddit APIs to conduct a sentiment analysis of the company
# associated with the stock. If the company is associated with positive sentiment that doesn't
# seem to be reflected in the price, it could be indicative of a buying opportunity
def accessStock(symbol):
    twitter_sentiment = twitter.findAvgSentiment(symbol)


def scanCrypto(symbol):
    # gets the information for the week and assign variables for the past two days
    past2 = rb.get_crypto_historical(symbol, 'day', 'week', '24_7')['data_points'][5]

    # information on the past day by the hour
    past_day = rb.get_crypto_historical(symbol, 'hour', 'day', '24_7')['data_points']

    # current price
    price_now = past_day[23]['close_price']
    print("Current price is: " + price_now)
    price_now = float(price_now)

    # price 5 hours ago
    price5 = past_day[18]['close_price']
    print("5 hours ago the price closed at: " + price5)
    price5 = float(price5)

    # price two days ago
    price2days = past2['open_price']
    print("2 days ago the price opened at: " + price2days)
    price2days = float(price2days)

    # calculating the two day change and the five hour change
    two_day_increase = (price_now - price2days) / price2days
    five_hour_increase = (price_now - price5) / price5

    if -0.12 < two_day_increase < -0.06 and 0 < five_hour_increase < 0.03:
        pass
    elif 0.09 < two_day_increase and -0.02 < five_hour_increase < 0:
        pass
