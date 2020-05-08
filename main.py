import robin_stocks as rb
import config

# import the username and password from the config.py file. If you choose to clone this
# repository and upload online, include the config.py file in gitignore to keep your information
# hidden
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


# function scans a cyptocurrency for a potential comeback, if a cryptocurrency has lost between 5
# and 12 percent of its value in the past 2 days, but has maintained a steady growth in the path 5
# hours, it could be indicative of a buying opportunity
def scanCrypto(symbol):
    # gets the information for the past day
    past2 = rb.get_crypto_historical(symbol, 'day', 'week', '24_7')['data_points'][5]
    past1 = rb.get_crypto_historical(symbol, 'day', 'week', '24_7')['data_points'][6]

    TwoAgoPrice = float(past2['open_price'])
    nowPrice = float(past1['close_price'])

    print((nowPrice - TwoAgoPrice) / TwoAgoPrice)


scanCrypto("BTC")

print(rb.get_crypto_info('ETH'))
