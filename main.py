import robin_stocks as rb
import config

# import the username and password from the config.py file. If you choose to clone this
# repository and upload online, include the config.py file in gitignore to keep your
# personal information hidden
username = config.userName
password = config.password

# login to robinhood
rb.login(username, password)

# list all available cryptocurrencies for purchase
print(rb.get_crypto_currency_pairs())

# Of those cryptos, print their symbols
for crypto in rb.get_crypto_currency_pairs():
    print(crypto['asset_currency']['code'])

# getting historical data from a cryptocurrency, particularly the performance each day for the past
# week
print(rb.get_crypto_historical("BTC", 'day', 'week', '24_7'))



def buyCrypto(symbol):
    pass


def sellCrypto(symbol):
    pass


def scanCrypto(symbol):
    # gets the information for the week and assign variables for the past two days
    past2 = rb.get_crypto_historical(symbol, 'day', 'week', '24_7')['data_points'][5]

    # information on the past day by the hour
    pastDay = rb.get_crypto_historical(symbol, 'hour', 'day', '24_7')['data_points']

    # current price
    priceNow = pastDay[23]['close_price']
    print("Current price is: " + priceNow)
    priceNow = float(priceNow)

    # price 5 hours ago
    price5 = pastDay[18]['close_price']
    print("5 hours ago the price closed at: " + price5)
    price5 = float(price5)

    # price two days ago
    price2days = past2['open_price']
    print("2 days ago the price opened at: " + price2days)
    price2days = float(price2days)

    # calculating the two day change and the five hour change
    TwoDayIncrease = (priceNow - price2days) / price2days
    FiveHourIncrease = (priceNow - price5) / price5

    if -0.12 < TwoDayIncrease < -0.06 and 0 < FiveHourIncrease < 0.03:
        buyCrypto(symbol)
    elif 0.09 < TwoDayIncrease and -0.02 < FiveHourIncrease < 0:
        sellCrypto(symbol)


scanCrypto("BTC")
