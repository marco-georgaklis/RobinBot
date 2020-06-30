import config
import praw
from textblob import TextBlob as tb

# accessing reddit API using praw wrapper
reddit = praw.Reddit(client_id=config.redditApp,
                     client_secret=config.redditSecret,
                     user_agent=config.redditUser)

# common subreddits for stock market discussions
stock_subreddits = ["stocks", "StockMarket", "options", "investing", "wallstreetbets", "all"]


# finding the average sentiment
def findAvgSentiment(word, sub, time_frame):
    total_polarity = 0
    count = 0

    for submission in reddit.subreddit(sub).search(word, "relevance", "lucene", time_frame):
        text = submission.selftext
        polarity = tb(text).sentiment.polarity
        total_polarity += polarity

        if polarity != 0:
            count += 1

    if count == 0:
        return 0

    return total_polarity / count


def scanStockSubs(symbol, time_frame):
    # total polarity value
    total_sentiment = 0

    for sub in stock_subreddits:
        sent = findAvgSentiment(symbol, sub, time_frame)
        total_sentiment += sent

    return total_sentiment / len(stock_subreddits)



