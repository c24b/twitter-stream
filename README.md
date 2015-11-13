# twitter-stream
Twitter library to stream data filter by #hastag


##Installation
1. Get your credential for '''streaming''' Twitter API
[Twitter Stream API documentation | https://dev.twitter.com/streaming/overview]
by creating a twitter app [ https://apps.twitter.com/ | twitter app page]


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
* the project info configuration: 
a database_name and the query

{"consumer_key" :'',
"consumer_secret" : '',
"access_token" : '',
"access_token_secret" : '',
"database_name": '',
"hashtag":''
}

## Stream it!

```
python tweestream.py
```

