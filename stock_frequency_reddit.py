import config
import praw
from datetime import date
import pandas as pd


# accessing reddit API using praw wrapper
reddit = praw.Reddit(client_id=config.redditApp,
                     client_secret=config.redditSecret,
                     user_agent=config.redditUser)


def potential_word_list(text, refined_words=None):
    
    if refined_words is None:
        refined_words = []
    stopwords = ['DD', 'US', 'AND', 'PR', 'CEO', 'EV', 'SO',
                 'IN', 'RH', 'FDA', 'OP', 'WSB', 'SPY']
    
    for word in text.split():
        if word[0] == '$':
            word = word[1:]
        
        if (2 <= len(word) <= 4 and word == word.upper()) and word not in stopwords:
            valid = True
            for char in word:
                if not char.isalpha():
                    valid = False
            if valid:
                refined_words.append(word)
            
    return refined_words        


def search_daily_thread(submission):
    """
    This function searches all the comments of 1 reddit post for stocks
    and calls the generate_frequency_dataframe() function to generate a
    frequency table of all the stocks mentioned
    """
    stock_list = []
    
    for comment in submission.comments:
        stock_list = potential_word_list(comment.body, stock_list)
    
    return generate_frequency_dataframe(stock_list)


def generate_frequency_dataframe(words):
    """
    function takes a list of words and creates a pandas
    dataframe in sorted order with all the words and 
    their frequencies
    """
    df = pd.DataFrame(words)
    df['freq'] = df[0].apply(lambda x: words.count(x))
    
    df.drop_duplicates(inplace=True)
    df.sort_values(by=['freq'], ascending=False, inplace=True)
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)
    
    return df


def generate_stock_list_from_sub(subreddit, post_number=500):
    """
    function generates a list of the most frequently talked about
    stocks in a given subreddit
    """
    words = []
    for submission in reddit.subreddit(subreddit).new(limit=post_number):
        words = potential_word_list(submission.selftext, words)

    return generate_frequency_dataframe(words)


def rpenny_daily_thread(today=None):
    """
    This function searches r/pennystocks for their "Tomorrow's Daily" thread. If it
    finds the thread, it searches the comments for stocks to see what the most popular
    picks are for tomorrow. Returns a dataframe with most frequently talked about stocks
    on the thread
    """
    # Create a new date object based on todays date and format accordingly
    if today is None:
        today = date.today()
    found = False

    # search r/pennystocks for Tomorrow's Daily thread
    for submission in reddit.subreddit("pennystocks").search(today.strftime("%B %d, %Y Tomorrow's "
                                                                            "Daily")):
        post = submission
        found = True
        print("Submission Found")
        break

    if not found:
        print("Error: Thread not found. Please try again.")
        return

    return search_daily_thread(post)



