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

def get_time(tup):
    return tup[0]

def get_tweet(tup):
    return tup[1]

# reogranizes tweets based on timecodes
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
def demo():
    response = input("Breaking or trending? ")
    if response == "breaking":
        filename = open("breaking.txt")
    elif response == "trending":
        filename = open("sources.txt")
    # gets most recent tweets from list of sources and reorganizes based on time
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
