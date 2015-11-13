# twitter-stream
Simple Twitter library to stream data filter by #hastag
stored in a csv file


##Installation
1. Get your credential for '''streaming''' Twitter API
(Twitter Stream API documentation | https://dev.twitter.com/streaming/overview)
by creating a twitter app (https://apps.twitter.com/ | twitter app page)


2. Install tweepy package
```
pip install tweepy
```
or install throught requirements.txt
```
pip install -r requirements.txt
```

3. Configure your project into config.json
with: 
* the credentials given into your twitter application
* the project info configuration:  a database_name and the query (#hashtag)
* if you want to filter on specific twitter accounts set a list of followed user account 
* set a timeout date to specify the end of the streaming archives (expressed in day format = dd/mm/yyyy)

{"consumer_key" :"",
"consumer_secret" : "",
"access_token" : "",
"access_token_secret" : "",
"database_name": "opencon",
"followed_users": false,
"hashtag":"#opencon",
"timeout_date":"18/11/2015"}

## Stream it!
In command line or in a cron
```
$ python tweestream.py &
```

