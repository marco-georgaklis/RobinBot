import config
import praw
from datetime import date
import pandas as pd
from nltk.corpus import stopwords

# non-stock symbol stopwords that aren't in the nltk corpus stopwords
stopwords2 = "THAT,WITH,BE,AS,YOU,DD,US,AND,PR,CEO,EV,SO,IN,RH,FDA,OP,WSB,SPY,TRUE,JOB,ONLY,TO," \
             "FOR,THE,MY,AT,THIS,SOME,BUT,ARE,LIKE,WILL,THAT,IT,ON,SEE,OR,HAVE,OF,IS,UP,THEY,IF," \
             "BY,WAS,NOT,HAS,ALL,JUST,FROM,WHAT,NEW,CAN,WE,DO,MORE,GOOD,BEEN,NEWS,OUT,ITS,OVER," \
             "ANY,OUR,JULY,TIME,GET,ALSO,lAST,KNOW,ONE,INTO,AM,HAD,YOUR,HOW,THAN,KEEP,WHEN,HERE," \
             "LIVE,WEEK,BY,TAKE,VERY,WHO,WANT,LOOK,MAKE,LOW,LAST,BUY,MAY,EVEN,WELL,MUCH,FIND,USE," \
             "GOT,FEW,WERE,BACK,GO,PLAY,DAY,YEAR,PART,SALE,CALL,NET,NEXT,BIG,MADE,POST,SORT,LOT," \
             "HIGH,LONG,MANY,GUYS,NEED,SELL,RUN,JUNE,DATA,LOSS,PAST,WENT,WAY,HOLD,TERM,WORK,PER," \
             "HELP,COME,FEEL,FORM,END,SOLD,ABLE,HUGE,GOLD,SAID,MOVE,DUE,SAY,NICE,FULL,OPEN,SEEN," \
             "HALF,SUB,SURE,DRUG,REAL,CASH,OTC,INFO,BEST,ELSE,HOPE,SHIT,YET,LOVE,PRE,PUMP,SOON," \
             "USER,HEY,USED,GIVE,GOLF,STOP,PUT,DAYS,CAME,READ,IM,CAP,HIT,DIP,LINK,BAD,GROW,FREE," \
             "GAIN,JUMP,BIT,PLAN,LET,BAG,TECH,DROP,FACT,RATE,AGO,RISK,APP,AI,GETS,LOST,RISE,TRY," \
             "SEEM,TOOK,MOON,SUN,FAR,LESS,SET,JUN,TWO,DEAL,HARD,RED,DATE,ETC,CASE,DONE,OIL,COST," \
             "LEAD,SAW,DONE,WAIT,EDGE,BANK,FAST,FOOD,TEST,STAY,HELD,LOSE,JOHN,DONT,BILL,VOTE,AIR," \
             "FALL"

sw = stopwords.words('english')
sw2 = stopwords2.split(',')



def login():
    """
    Accessing reddit API using praw wrapper, returns a reddit instance
    """
    return praw.Reddit(client_id=config.redditApp,
                       client_secret=config.redditSecret, user_agent=config.redditUser)


def potential_word_list(text, refined_words=None):
    """
    This function takes in a document or corpus of text that needs to
    be searched for stock symbols and refined_words: a list of
    potential stock symbols that have already been extracted
    from some text. It returns the refined_words list with all potential stock
    symbols from the text added to it
    """
    if refined_words is None:
        refined_words = []

    for word in text.split():
        if word[0] == '$':
            word = word[1:]
        if len(word) > 2 and word[-1] == ',':
            word = word[:-1]

        word = word.lower()
        if 2 <= len(word) <= 4 and word not in sw and word.upper() not in sw2:
            valid = True
            for char in word:
                if not char.isalpha():
                    valid = False
            if valid:
                refined_words.append(word.upper())

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


def generate_stock_list_from_sub(reddit=login(), subreddit="pennystocks", post_number=500):
    """
    function generates a list of the most frequently talked about
    stocks in a given subreddit
    """
    words = []
    for submission in reddit.subreddit(subreddit).new(limit=post_number):
        words = potential_word_list(submission.selftext, words)

    return generate_frequency_dataframe(words)


def rpenny_daily_thread(reddit, today=None):
    """
    This function searches r/pennystocks for their "Tomorrow's Daily" thread. If it
    finds the thread, it searches the comments for stocks to see what the most popular
    picks are for tomorrow. Returns a dataframe with most frequently talked about stocks
    on the thread
    """
    # Create a new date object based on todays date and format accordingly
    if today is None:
        today = date.today()
    post = None

    # search r/pennystocks for Tomorrow's Daily thread
    for submission in reddit.subreddit("pennystocks").search(today.strftime("%B %d, %Y Tomorrow's "
                                                                            "Daily")):
        post = submission
        print("Submission Found")
        break

    if post is None:
        print("Error: Thread not found. Please try again.")
        return

    return search_daily_thread(post)
