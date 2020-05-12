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
def findAvgSentiment(word, sub):
    total_polarity = 0
    count = 0

    for submission in reddit.subreddit(sub).search(word, "relevance", "lucene", "day"):
        text = submission.selftext
        polarity = tb(text).sentiment.polarity
        total_polarity += polarity
        count += 1

    if count == 0:
        return 0

    return total_polarity / count


for subreddit in stock_subreddits:
    print(subreddit)
    print(findAvgSentiment("Elon Musk", subreddit))
