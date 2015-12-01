# Python wrapper for Twitter API
import tweepy

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
