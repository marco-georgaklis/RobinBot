from stock_frequency_reddit import *
import config
import robin_stocks


def find_penny_stocks_to_buy(date=None, threshold=10):
    """
    This function searches r/pennystocks for the most mentioned
    penny stocks in the 'Tomorrow's Picks' thread. It accepts a date
    to use in the thread search and a threshold for the number of
    mentions the stock needs to be relevant to the user.

    """

    reddit = login()
    r_penny = rpenny_daily_thread(reddit, date)
    r_penny = r_penny[r_penny['freq'] > threshold]

    if len(r_penny) > 0:
        print(f"{len(r_penny)} potential buys found for today!")
    else:
        print("No viable stocks found for today")
    return r_penny


def buy_predicted_stocks(stock_df, amount_to_spend=20):
    """
    This function takes in the pandas stock dataframe created in the find_penny_stocks_to_buy
    method and the amount of money the user wants to spend and uses the robin_stocks library to
    place orders for each stock
    """

    # calculate amount to allocate to each stock
    amount_per_stock = amount_to_spend / len(stock_df)

    for i in range(0, len(stock_df)):
        symbol = stock_df[0][i]
        found = False
        for stock in robin_stocks.stocks.find_instrument_data(symbol):

            if stock['symbol'] == symbol and stock['tradeable']:
                found = True
                break

        if found:
            price = float(robin_stocks.stocks.get_latest_price(symbol)[0])
            shares = amount_per_stock // price

            print(f"Buying {shares} shares of {symbol} at {price}")

            # uncomment line below to place order
            # robin_stocks.order_buy_market(symbol, shares)
        else:
            print(f"Error: {symbol} not found on Robinhood")


def run_reddit_bot(money=20):
    """
    This function takes in the amount of money the user wants to invest in stocks for today and
    and then uses the money to execute trades if the program finds viable stock investments for
    today
    """

    stock_df = find_penny_stocks_to_buy()

    if stock_df:
        buy_predicted_stocks(stock_df, money)
    else:
        print("No stocks found for today, try again")


# import the username and password from the config.py file. If you choose to clone this
# repository and upload online, include the config.py file in gitignore to keep your
# personal information hidden
username = config.robinUser
password = config.robinPassword

# login to Robinhood
robin_stocks.login(username, password)

# determine the amount of money in your account you want the bot to invest in for today,
# it is currently set to 20
amount = 20

# Run the bot. To actually purchase the stocks, uncomment the buy_market call in
# buy_predicted_stocks method
run_reddit_bot(amount)
