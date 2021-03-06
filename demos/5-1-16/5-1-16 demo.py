# demo assumes tweets in separate text file!
import emoji
from datetime import datetime
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
from vincenty import vincenty
from decimal import *
import re

tweets_organized = []
entries = []
tweets = {}
sources = {}
hashtags = {}
urls = {}
geolocator = GoogleV3()

saved_locations = { 'Dallas, TX' : (32.7766642, -96.79698789999998), 'New York, NY' : (40.7127837, -74.00594130000002), 'Chicago, IL' : (41.8781136, -87.62979819999998),
                    'Flint, MI' : (43.0125274, -83.68745619999999), 'Boston, MA' : (42.3600825, -71.05888010000001), 'Seattle, WA' : (47.6062095, -122.3320708),
                    'Los Angeles, CA' : (34.0522342, -118.2436849), 'London, UK' : (34.0522342, -118.2436849), 'Washington, D.C.' : (38.9071923, -77.03687070000001),
                    'Nashville, TN' : (38.9071923, -77.03687070000001), 'Orlando, FL' : (28.5383355, -81.37923649999999) , 'Austin, TX' : (30.267153, -97.74306079999997),
                    'Houston, TX' : (29.7604267, -95.3698028), 'Lebanon, KS' : (39.8097343, -98.55561990000001), 'St. Louis, MO' : (38.62700249999999, -90.1994042),
                    'San Diego, CA' : (32.715738, -117.16108380000003), 'Detroit, MI' : (42.33142699999999, -83.0457538), 'Kansas City, KS' : (39.11405299999999, -94.6274636), 
                    'Phoenix, AZ' : (33.4483771, -112.07403729999999), 'Doha, Qatar' : (25.2854473, 51.53103979999992), 'Atlanta, GA' : (33.7489954, -84.3879824),
                    'Ottawa, ON' : (33.7489954, -84.3879824), 'Fort Worth, TX' : (32.7554883, -97.3307658), 'Long Island, NY' : (40.789142, -73.13496099999998),
                    'Paris, France' : (48.856614, 2.3522219000000177), 'Denver, CO' : (39.7392358, -104.990251), 'Portland, OR' : (45.52306220000001, -122.67648159999999),
                    'Philadelphia, PA' : (39.9525839, -75.16522150000003), 'San Francisco, CA' : (37.7749295, -122.41941550000001), 'San Jose, CA' : (37.3382082, -121.88632860000001),
                    'Indianapolis, IN' : (39.768403, -86.15806800000001), 'Columbus, OH' : (39.9611755, -82.99879420000002), 'Charlotte, NC' : (39.9611755, -82.99879420000002),
                    'Baltimore, MD' : (39.2903848, -76.61218930000001), 'Las Vegas, NV' : (36.1699412, -115.13982959999998), 'Salt Lake City, UT' : (40.7607793, -111.89104739999999),
                    'Cleveland, OH' : (41.49932, -81.69436050000002), 'Arlington, TX' : (32.735687, -97.10806559999997), 'Arlington, VA' : (38.8799697, -77.1067698),
                    'New Orleans, LA' : (29.95106579999999, -90.0715323),  'Honolulu, HI' : (21.3069444, -157.85833330000003), 'Rochester, NY' : (43.16103, -77.6109219),
                    'McLean, VA' : (38.93386760000001, -77.17726040000002), 'Silver Spring, MD' : (38.99066570000001, -77.02608800000002),  'Boca Raton, FL' : (26.3683064, -80.12893209999999), 
                    'Cambridge, MA' : (42.3736158, -71.1097335), 'Columbia, MI' : (38.95170529999999, -92.33407239999997), 'Doral, FL' : (25.8195424, -80.35533020000003),
                    'Hastings, NE' : (40.5862583, -98.38987259999999), 'Lincoln, NE' : (40.8257625, -96.6851982), 'Upton, NY' : (40.8682379, -72.8791716), 'New Brunswick, NJ' : (40.4862157, -74.45181880000001) } 

def demo():
    tweet_count = 0
    total_tweets = 0
    organize_sources()
    recency, locality, trend = user_inputs()
    current_location = input("Enter a location (example -> Los Angeles, CA or Chicago, IL): ")
    # returns coordinates of user-input location as a tuple
    current_coords = get_location_coordinates(current_location)
    current_time = get_current_time()
    filename = input("Enter a filename: ")
    f = filename + ".txt"
    try:
        file = open(f)
    except Exception:
        f = input("Oops, that file didn't work. Try again: ")
        f = f + ".txt"
        file = open(f)
    print("\n")
    for line in file:
        total_tweets = total_tweets + 1
        # in case anything fails
        try:
            author, entry, time, coord = line.rstrip("\n").split("~~")
##            print(entry)
##            add_url(entry)
##            add_hashtag(entry)
            recency_rank = get_recency_ranking(time, current_time)
            # should always be true
            if author in sources:
                t = sources[author]
                source_location = get_first(t)
                trend_rank = float(get_second(t))
                flag = get_third(t)
                location_rank = get_location_ranking(source_location, current_coords, coord, flag)
            tweet_total = calculate_total_ranking(recency, locality, trend, recency_rank, location_rank, trend_rank)
            if tweet_total in tweets:
               tweet_total = tweet_total + 0.000001
            tweets[tweet_total] = [entry, author, time]
            tweet_count = tweet_count + 1
        except Exception:
            print("Sorry, couldn't load tweet.\n")
    organize_tweets()
    file.close()
    print_tweets_from_list(tweets_organized)
    print("%d tweets out of %d loaded" % (tweet_count, total_tweets))
##    print(hashtags)
##    print(urls)
    clear()

def clear():
    del tweets_organized[:]
    tweets.clear()
    hashtags.clear()
    urls.clear()

def print_tweets_from_list(ls):
    for item in ls:
        e = get_first(item)
        a = get_second(item)
        t = get_third(item)
        print("%s @ %s: %s\n" % (a, t, e))

def organize_sources():
    s = input("Enter source file: ")
    s = s + ".txt"
    sources_text = open(s)
    for line in sources_text:
        handle, user_location, trend_rank, location_flag = line.rstrip("\n").split(";")
        sources[handle] = user_location, trend_rank, location_flag
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

def add_url(string):
    entry_url = re.findall(r'(https?://[^\s]+)', string)
    for i in entry_url:
        if i in urls:
            urls[i] = urls[i] + 1
        else:
            urls[i] = 1

def add_hashtag(string):
    entry_hashtags = re.findall(r"(#[\w]*", string)
    for x in entry_hashtags:
        if x in entry_hashtags:
            hashtags[x] = hashtags[x] + 1
        else:
            hashtags[x] = 1

def add_entry(string):
    if string in entries:
        pass
    else:
        entries.append(string)
       
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
        return 0.7
    elif 6 <= hours < 12:
        return 0.6
    elif 12 <= hours < 18:
        return 0.5
    elif 18 <= hours < 24:
        return 0.4
    elif 24 <= hours < 36:
        return 0.3
    else:
        return 0.2

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

def check_flag(flag):
    if flag == "global" or flag == "national":
        return 0.15
    
def get_location_coordinates(location):
    if location in saved_locations:
        coords = saved_locations[location]
        return coords
    else:
        try:
            gps = geolocator.geocode(location)
            lat, long = gps.latitude, gps.longitude
            coords = (gps.latitude, gps.longitude)
            saved_locations[location] = coords
            return coords
        except Exception:
            pass

def get_location_ranking(source, current, tweet, flag):
    if flag == "global" or flag == "national":
        return 0.00079228162
    else:
        source_coords = get_location_coordinates(source)
        if tweet == "None":
            try:
                dist = vincenty(source_coords, current).miles
            except Exception:
                dist = vincenty(source_coords, current)
        else:
            try:
                dist = vincenty(tweet, current).miles
            except Exception:
                dist = vincenty(tweet, current)
        # based on distance, return ranking
        if dist <= 1:
            return 0.9
        elif 1 < dist < 10:
            return 0.8
        elif 10 <= dist < 20:
            return 0.7
        elif 20 <= dist < 50:
            return 0.6
        elif 50 <= dist < 100:
            return 0.5
        elif 100 <= dist < 200:
            return 0.4
        elif 200 <= dist < 300:
            return 0.3
        elif 300 <= dist < 400:
            return 0.2
        else:
            return 0.1

def user_inputs():
    recency = float(input("On a scale of 1 to 3 (one as most important), how important is recency? "))
    locality = float(input("On a scale of 1 to 3 (one as most important), how important is locality? "))
    trend = float(input("On a scale of 1 to 3 (one as most important), how important is breaking news? "))
    return recency, locality, trend

def get_first(l):
    return l[0]

def get_second(l):
    return l[1]

def get_third(l):
    return l[2]

def get_fourth(l):
    return l[3]
