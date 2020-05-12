import config
import tweepy
from textblob import TextBlob as tb

# use api keys and access tokens to access twitter api using tweepy library
auth = tweepy.OAuthHandler(config.apiKey, config.apiSecretKey)
auth.set_access_token(config.accessToken, config.secretAccessToken)

api = tweepy.API(auth)

# find the average polarity of the most recent tweets that use the parameter word to determine if
# twitter looks at the word in a generally positive or negative light
def findAvgSentiment(word):
    # find all public tweets containing the word
    public_tweets = api.search(word)

    # the sum of all the polarity values of every tweet
    total_polarity = 0

    # the total number of tweets queried
    tweet_count = float(0)

    # for every tweet in the query
    for tweet in public_tweets:
        # get sentiment values from textblob
        polarity = tb(tweet.text).sentiment.polarity

        # add them to the total values

        total_polarity += polarity

        # increment tweet count
        tweet_count += 1

    avg_polarity = total_polarity / tweet_count

    return avg_polarity


def historicalSentiment(word):
    pass