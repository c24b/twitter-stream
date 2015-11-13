#usr/bin python env
import sys
import os
import json
import datetime
import tweepy
import csv
import re

def config(afile="config.json"):
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
        with open(DATASTORE, "a") as f:
            spamwriter = csv.writer(f, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(data)
    
    def on_status(self, status):        
        # We'll simply append some values in row (list)
        # suitable for writing into a csv file
        # and store it into database_name csv file
        
        try:
            row = [re.sub("\t|\n|\r", "", (status.text).encode('utf-8')), re.sub("\t|\n|\r", "", (status.author.screen_name).encode('utf-8')), status.created_at, re.sub("\t|\n|\r", "", status.source.encode('utf-8'))]
            #row = [re.sub("\t|\n|\r", "", str(n)) for n in row]
            #print(row)
            #yield row
            self.write_data(row)
            
            #print self.results
            #~ print len(raw)
            #~ print "\n"
        except Exception as e:
            
            print('Encountered Exception: %s' %e)
            pass

    def on_error(self, status_code):
        print('Encountered Exception: %s' %status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print('Timeout...')
        return True # Don't kill the stream
                
def run(params):
    
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

    
    
