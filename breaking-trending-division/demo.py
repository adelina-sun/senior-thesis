# Python wrapper for Twitter API
import tweepy
# still crashing when emojis encountered
import emoji
from datetime import datetime

# retrieve from http://dev.twitter.com/apps
# need to authenticate and approve application's access to account
consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

screen_name = ""
since_id = ""
max_id = ""
count = 20
page = 1
tweet_info = []
tweets_organized = []
sources = []

def get_time(tup):
    return tup[0]

def get_tweet(tup):
    return tup[1]

def get_current_time():
    return datetime.now()

# unfinished - currently prints timedelta object
def get_ranking(tweet_time, current_time):
    # creates timedelta object
    tdelta = current_time - tweet_time
    print(tdelta + "\n")
    # compare difference in dates
    # if tdelta < -1 days:
    # return ranking
    # else:
    # return other ranking

# reorganizes tweets based on timecodes
def compare_times(old_list, new_list, tup):
    if len(old_list) == 0:
        new_list.append(tup)
    elif get_time(old_list[-1]) < get_time(tup):
        info = old_list.pop()
        new_list.append(info)
        compare_times(old_list, tup)
    else:
        new_list.append(tup)

# does not associate tweet with source currently
# takes list of sources and organizes first few tweets from timeline by time
def demo():
    response = input("Breaking or trending? ")
    if response == "breaking":
        filename = open("breaking.txt")
    elif response == "trending":
        filename = open("sources.txt")
    for line in filename:
        screen_name = filename.readline()
        results = api.user_timeline(screen_name)
        for result in results:
            entry, entry_date = result.text, result.created_at
            t = (entry_date, entry)
            compare_times(tweet_info, tweets_organized, t)
    filename.close()
    for i in tweets_organized:
        print(get_tweet(i) + "\n")

# testing search
def search():
    q = input("Enter a search term: ")
    cursor = tweepy.Cursor(api.search, q)
    for tweet in cursor.items(100):
        print(tweet.text)

# builds search string and then uses cursor to search for the first 100 items & organizes by time
def demo_with_search():
    response = input("Breaking or trending? ")
    if response == "breaking":
        filename = open("breaking.txt")
    elif response == "trending":
        filename = open("sources.txt")
    q = input("Enter a search term: ")
    for line in filename:
        sources.append(line.strip())
    search_for_str = q + " AND " + "from:%s" % sources[0]
    for source in sources[0:]:
        search_for_str = search_for_str + " OR " + "from:%s" % source
    filename.close()
    results = tweepy.Cursor(api.search, search_for_str).items(100)
    for tweet in results:
        entry, entry_date = tweet.text, tweet.created_at
        t = (entry_date, entry)
        compare_times(tweet_info, tweets_organized, t)
    for i in tweets_organized:
        print(get_tweet(i) + "\n")

# testing timedelta    
def test():
    results = api.home_timeline()
    current = get_current_time()
    for result in results:
        result_time = result.created_at
        get_ranking(result_time, current)
