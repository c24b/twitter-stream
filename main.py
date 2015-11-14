#usr/bin python env
 # -*- coding: utf-8 -*-
import sys
import os
import json
import datetime
import tweepy
import csv
import re
from collections import OrderedDict, defaultdict
import codecs 

def config(afile="local_config.json"):
    '''load config given JSON file'''
    if afile.endswith("json"):
        curr_dir = os.getcwd()
        afile = os.path.join(curr_dir, afile)
        try:
            with open(afile) as json_f:
                try:
                    params = json.load(json_f)
                    end_day = datetime.datetime.strptime(params["timeout_date"], "%d/%m/%Y")
                    start_day = datetime.datetime.now()
                    params["timeout"] = int(round((end_day - start_day).total_seconds()))
                    params["db_path"] = os.path.join(os.getcwd(), params["database_name"]+".csv")
                    return params
                except ValueError as e:
                    return sys.exit("Error parsing config file %s: %s" %(afile,e))
        except IOError:
            return sys.exit("Config file %s not fount" %(afile))

    
                    
cfg = config()
DATASTORE = cfg["db_path"]

class CustomStreamListener(tweepy.StreamListener):
    
    def write_data(self,data):
        with codecs.open(DATASTORE, 'a', encoding='utf-8') as f:
        #with open(DATASTORE, "a") as f:
            #f.write("\t".join([repr(n) for n in data])+"\n")
            w = csv.writer(f, delimiter='\t')
            w.writerow(data)
            
    def extract(self, status):
        #extract author_info
        user = {
                "user_id":status.author.id,
                "user_location": status.author.location, 
                "user_name": status.author.name,
                "user_screen_name": status.author.screen_name,
                "user_url": status.author.url,
                'time_zone': status.author.time_zone,
                "user_description": status.author.description,
                "utc": status.author.utc_offset,
                "followers_count":status.author.followers_count,
                "friends_count":status.author.friends_count, 
                }
        for k, v in user.items():
            if v is None:
                user[k] = ("None").encode("utf-8")
            elif isinstance(v, unicode):
                    
                user[k] = v.encode("utf-8", "ignore")
                
            else:
                pass
        
        tweet = {
                'text':status.text.encode("utf-8"), 
                'reply_to_tweet_id': status.in_reply_to_status_id,
                'reply_to_screen_name': status.in_reply_to_screen_name,
                'reply_to_user_id': status.in_reply_to_user_id,
                'retweet_nb': status.retweet_count,
                'id': status.id,
                'from_source': status.source, 
                #'coordinates':status.coordinate, 
                #'retweeted_status': status.retweeted_status,
                'source_url': status.source_url,
                #'geo': status.geo,
                'lang':status.lang,
                #'tweet_created_at': status.create_at,
                'place': status.place,
                #'retweeted_status':status.retweeted_status,
                }
        
        for k, v in tweet.items():
            if v is None:
                user[k] = "None"
            elif isinstance(v, unicode):
                user[k] = v.encode('utf-8', "ignore")
                
               
            elif isinstance(v, (list,dict,tuple)):
                del user[k]
            else:
               pass
        user.update(tweet)
        return OrderedDict(sorted(user.items()))
        
        
    def on_status(self, status):        
        # We'll simply append some values in row (list)
        # suitable for writing into a csv file
        # and store it into database_name csv file
        
        try:
            d = self.extract(status)
            self.write_data(d.values())
        except Exception, e:
            self.write_data([repr(d) for d in d.values()])
            print "Warning extraction", e
            pass
            

    def on_error(self, status_code):
        if status_code == 420:
            print ("Enhance Your Calm. You rate has been limited")
        elif status_code == 503:
            print ('Service Unavailable The Twitter servers are up, but overloaded with requests. Try again later.')
        else:
            print('Encountered Exception: %s' %status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print('Timeout...')
        return False # Don't kill the stream
                
def run(params):
    #~ header = ["author."+n for n in ['created_at', 'description', 'favourites_count', 'follow_request_sent', 'followers_count', 'following', 'friends_count', 'id', 'id_str', 'lang', 'listed_count', 'location', 'name', 'screen_name', 'statuses_count', 'time_zone', 'url', 'utc_offset', 'verified']]
    #~ print header
    keys = ['followers_count', 'friends_count', 'from_source', 'id', 'lang', 'place', 'reply_to_screen_name', 'reply_to_tweet_id', 'reply_to_user_id', 'retweet_nb', 'source_url', 'text', 'time_zone', 'user_description', 'user_id', 'user_location', 'user_name', 'user_screen_name', 'user_url', 'utc']
    with codecs.open(DATASTORE, 'w', encoding='utf-8') as f:
        spamwriter = csv.writer(f, delimiter='\t')
        spamwriter.writerow(keys)

    #run stream
    query = params["hashtag"]
    
    auth = set_credentials(params)
    # Create a streaming API and set a timeout value based on end_date.
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=params["timeout"])
    # Optionally filter the statuses you want to track by providing a list
    # of users to "follow".
    follow = params["followed_users"]
    if follow is False:
        streaming_api.filter(follow=None, track=[query]) 
    else:
        streaming_api.filter(follow=follow, track=[query]) 
    #streaming_api.filter(follow=None, track=Q)
        

    
def set_credentials(params):
    # Get these values from your application settings and set it into your config file
    auth = tweepy.OAuthHandler(params["consumer_key"], params["consumer_secret"])
    auth.set_access_token(params["access_token"], params["access_token_secret"])
    return auth
    # Note: Had you wanted to perform the full OAuth dance instead of using
    # an access key and access secret, you could have uses the following 
    # four lines of code instead of the previous line that manually set the
    # access token via auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET).
    #import webbrowser
    # 
    # auth_url = auth.get_authorization_url(signin_with_twitter=True)
    # webbrowser.open(auth_url)
    # verifier = raw_input('PIN: ').strip()
    # auth.get_access_token(verifier)

    
def stream():
    run(cfg)   

    
    
