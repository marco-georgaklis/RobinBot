import robin_stocks as rb
import config
import twitter
import reddit

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
    # get ceo name of stock symbol
    ceo = rb.get_fundamentals(symbol)[0]['ceo']

    # quantify public sentiment around ceo
    twitter_ceo_pol = twitter.findAvgSentiment(ceo)
    reddit_ceo_pol = reddit.findAvgSentiment(ceo, "all", "day")
    print(ceo, "has sentiment of", twitter_ceo_pol, "on twitter and", reddit_ceo_pol, "on reddit")





accessStock("TSLA")
