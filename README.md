# twitter-stream
Simple Twitter library to stream data filter by #hastag
stored in a csv file


##Installation
1. Get your credential for '''streaming Twitter API''':
by creating a twitter app  on twitter app page : https://apps.twitter.com/

* See Twitter Stream API documentation for more info: https://dev.twitter.com/streaming/overview

* To extend current package take a look at the brillant 
```tweepy``` module: https://github.com/tweepy/tweepy

2. Install tweepy package
```
pip install tweepy
```
or install throught requirements.txt
```
pip install -r requirements.txt
```

3. Configure your project into ```config.json``` file
with: 
* the credentials given into your twitter application
* the project info configuration:  a database_name and the query (#hashtag)
* if you want to filter on specific twitter accounts set a list of followed user account 
* set a timeout date to specify the end of the streaming archives (expressed in day format = dd/mm/yyyy)

```
{"consumer_key" :"",
"consumer_secret" : "",
"access_token" : "",
"access_token_secret" : "",
"database_name": "opencon",
"followed_users": false,
"hashtag":"#opencon",
"timeout_date":"18/11/2015"}
```

## Stream it!
In command line or in a cron
```
$ python streamtweet.py &
```

