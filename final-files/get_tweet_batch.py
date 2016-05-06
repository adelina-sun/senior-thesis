# calls Twitter search and collects tweets, storing them locally in new text file
# due to Twitter Rate Limits, can only be called once every fifteen minutes
# Python wrapper for Twitter API
import tweepy
import emoji
from datetime import datetime, date

# OAuth
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

def get_tweet_batch():
    search = input("Enter a search term: ")
    source_file = input("Enter a source file: ")
    source_file = source_file + ".txt"
    sources_file = open(source_file)
    new_file = input("Enter a name for your new file: ")
    filename = new_file + ".txt"
    ref_file = open(filename, "w")
    for line in sources_file:
        username, hq, trendiness, location_flag = line.split(";")
        q = search + " AND " + "from:%s" % username
        cursor = tweepy.Cursor(api.search)
        t = api.search(q, result_type = ["mixed"], count = [20])
        try:
            for tweet in t:
                author, entry, time, coord = username, tweet.text, str(tweet.created_at), str(tweet.coordinates)
                entry = entry.replace("\n", " ")
                ref_file.write("%s~~%s~~%s~~%s\n" % (author, entry, time, coord))
        except Exception:
            print("Encountered an error with Twitter!")
            break
    ref_file.close()
    sources_file.close()
