# gets tweets based on keyword and saves them & information locally in text file

# Python wrapper for Twitter API
import tweepy
# still crashing when emojis encountered
import emoji
from datetime import datetime, date
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty

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

sources = []

def get_date():
    now = date.today()
    date_string = str(now)
    return date_string

def retrieve_tweets():
    search = input("Enter a search term: ")
    sources_file = open("full_sources.txt")
    date = get_date()
    filename = search + " " + date
    filename = filename + ".txt"
    ref_file = open(filename, "w")
    for line in sources_file:
        username, hq, trendiness = line.split(";")
        sources.append(username)
        q = search + " AND " + "from:%s" % username
        cursor = tweepy.Cursor(api.search, q)
        for tweet in cursor.items(20):
            author, entry, time, coord = username, tweet.text, str(tweet.created_at), str(tweet.coordinates)
            # print(author + "; " + entry + "; " + time + "; " + coord + "\n")
            ref_file.write("%s;%s;%s;%s\n" % (author, entry, time, coord))
    ref_file.close()
    sources_file.close()
        
