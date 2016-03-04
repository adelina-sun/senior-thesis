# assumes tweets are saved locally in text file

# Python wrapper for Twitter API
import tweepy
# still crashing when emojis encountered
import emoji
from datetime import datetime
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
from decimal import *

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

screen_name = ""
since_id = ""
max_id = ""
count = 20
page = 1
tweets_organized = []
tweets = {}
sources = {}
geolocator = GoogleV3()

# not putting all tweets into list
def demo():
    organize_sources()
    recency, locality, trend = user_inputs()
    # returns coordinates of user-input location as a tuple
    current_coords = get_current_coordinates()
    current_time = get_current_time()
    f = input("Enter a filename: ")
    file = open(f)
    for line in file:
        author, entry, time, coord = line.rstrip("\n").split(";")
        recency_rank = get_recency_ranking(time, current_time)
        # should always be true
        if author in sources:
            t = sources[author]
            source_location = get_first(t)
            trend_rank = float(get_second(t))
            location_boolean = if_location(coord)
            if location_boolean == 0:
                location_rank = location_ranking_with_location(source_location, current_coords)
            else:
                location_rank = location_ranking_with_coord(coord, current_coords)
        tweet_total = calculate_total_ranking(recency, locality, trend, recency_rank, location_rank, trend_rank)
        # tweet_info = [entry, author, time, tweet_total]
        if tweet_total in tweets:
            tweet_total = tweet_total + 0.000001
        tweets[tweet_total] = [entry, author, time]
        # organize_tweet(tweet_info, tweets_organized)
        # tweets.append(tweet_info)
    # doesn't sort by RANKING (because nested list, need a way to sort by fourth item in nested list)
    # tweets_organized.sort()
    organize_tweets()
    file.close()
    print_tweets_from_list(tweets_organized)
    clear()

def clear():
    del tweets_organized[:]
    tweets.clear()

def print_tweets_from_list(ls):
    for item in ls:
        e = get_first(item)
        a = get_second(item)
        t = get_third(item)
        print("%s @ %s: %s\n" % (a, t, e))

def organize_sources():
    sources_text = open("full_sources.txt")
    for line in sources_text:
        handle, user_location, trend_rank = line.rstrip("\n").split(";")
        sources[handle] = user_location, trend_rank
    sources_text.close()
        
def calculate_total_ranking(recency, locality, trend, recency_rank, locality_rank, trend_rank):
    recency_weight = recency_rank**recency
    locality_weight = locality_rank**locality
    trend_weight = trend_rank**trend
    total_weight = recency_weight + locality_weight + trend_weight
    return total_weight

def organize_tweets():
    sorted_tweets = sorted(tweets)
    for i in sorted_tweets:
        tweet_info = tweets[i]
        tweets_organized.insert(0, tweet_info)

# tried sorting recursively, but not inserting past two items in list
def organize_tweet(tweet_info, ls):
    total = get_fourth(tweet_info)
    if len(ls) == 0:
        ls.append(tweet_info)
    elif total > get_fourth(ls[0]):
        ls.insert(0, tweet_info)
    else:
        ls + organize_tweet(tweet_info, ls[1:])

def get_current_time():
    return datetime.now()

def get_recency_ranking(tweet_time, current_time):
    # converts time string back to datetime
    tweet_datetime = datetime.strptime(tweet_time, "%Y-%m-%d %H:%M:%S")
    # creates timedelta object
    tdelta = current_time - tweet_datetime
    seconds = tdelta.seconds
    hours = seconds // 3600
    if hours < 1:
        minutes = seconds // 60
        return 0.9
    elif 1 <= hours < 3:
        return 0.8
    elif 3 <= hours < 6:
        return 0.64
    elif 6 <= hours < 12:
        return 0.4096
    elif 12 <= hours < 18:
        return 0.16777216
    elif 18 <= hours < 24:
        return 0.02814749767
    else:
        return 0.00079228162

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
    
def get_current_coordinates():
    current_location = input("Enter a location: ")
    current_gps = geolocator.geocode(current_location)
    current_lat, current_long = current_gps.latitude, current_gps.longitude
    current_coords = (current_gps.latitude, current_gps.longitude)
    return current_coords

def if_location(tweet_coord):
    if tweet_coord == "None":
        return 0
    else:
        return tweet_coord

def location_ranking_with_location(source_location, current_coords):
    location_gps = geolocator.geocode(source_location)
    location_lat, location_long = location_gps.latitude, location_gps.longitude
    source_coord = (location_lat, location_long)
    # calculates the difference in distance
    dist = vincenty(source_coord, current_coords).miles
    # return dist
    if dist <= 1:
        return 0.8
    elif 1 < dist < 10:
        return 0.64
    elif 10 <= dist < 20:
        return 0.4096
    elif 20 <= dist < 30:
        return 0.16777216
    elif 30 <= dist < 40:
        return 0.02814749767
    elif 40 <= dist < 50:
        return 0.00079228162
    else:
        return 0.00000062771

# assumes locations already in gps coordinates
def location_ranking_with_coord(tweet_coords, current_coords):
    # calculates the difference in distance
    dist = vincenty(tweet_coords, current_coords).miles
    # return dist
    if dist <= 1:
        return 0.8
    elif 1 < dist < 10:
        return 0.64
    elif 10 <= dist < 20:
        return 0.4096
    elif 20 <= dist < 30:
        return 0.16777216
    elif 30 <= dist < 40:
        return 0.02814749767
    elif 40 <= dist < 50:
        return 0.00079228162
    else:
        return 0.00000062771

def user_inputs():
    recency = float(input("On a scale of 1 to 3 (three as most important), how important is recency? "))
    locality = float(input("On a scale of 1 to 3 (three as most important), how important is locality? "))
    trend = float(input("On a scale of 1 to 3 (three as most important), how important is breaking news? "))
    return recency, locality, trend

def get_first(l):
    return l[0]

def get_second(l):
    return l[1]

def get_third(l):
    return l[2]

def get_fourth(l):
    return l[3]
