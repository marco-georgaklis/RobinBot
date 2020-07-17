# Robinhood Stock Trading Bot
This program uses the robin_stocks library to interact with the robinhood API. It works by searching reddit subreddits, particularly r/pennystocks, for the most popular buys for tomorrow. The find_penny_stocks_to_buy method searches the daily threads for that particular day for tomorrow's predictions.

In main.py, the user specifies the amount of money they want to invest, and the the money is distributed equally among the viable stocks found. Initially, I had it weighted towards the stocks that were most heavily mentioned, but found the program yielded the best results when there was a threshold for mentions and all the stocks that met the threshhold received equal funding.

I ran this program either at the end of trading hours or during extended hours. Extended hours can be difficult because of low volume, so switching the market order to a limit order may be useful. I sold during the next day, when I was satisfied with my gain.
##Clone repository
```
git clone 
```

## Open main.py
Replace username and password with your username and password for Robinhood
```
username = YOUR_ROBINHOOD_USERNAME
password = YOUR_ROBINHOOD_PASSWORD
```
Determine the amount of money (dollars) you want to invest today
```
amount = 50
```
Adjust the threshhold accordingly. The threshold for mentions to buy is automatically set at 10, but this is on the more conservative side, and often the bot won't buy any stocks. The lower the threshold, the more stocks, but the more risky the results.

```
ind_penny_stocks_to_buy(date=None, threshold=MENTIONS_YOU WANT)
```
## Open stock_frequency_reddit.py
Change login() function to have your personal reddit info. If you have not set up a reddit application, use https://www.reddit.com/dev/api/ for help. You should receive an App ID, a secret key, and know your username. 
```
return praw.Reddit(client_id=config.APP_ID,
                   client_secret=SECRET_KEY,
                   user_agent=REDDIT_USERNAME)
```
Run it and see how it goes!
## Using different subreddits
In stock_frequency_reddit.py, the generate_stock_list_from_sub allows you to explore the popular stock options in other subreddits. Be careful with subs like r/options, where people also invest in puts and are actually predicting the stock will decrease in price

