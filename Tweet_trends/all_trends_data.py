# import tweepy
# import pandas as pd
# import os

# #Twitter Access
# auth = tweepy.OAuthHandler( 'xxx','xxx')
# auth.set_access_token('xxx-xxx','xxx')
# api = tweepy.API(auth,wait_on_rate_limit = True)

# df = pd.DataFrame(columns=['text', 'source', 'url'])
# msgs = []
# msg =[]

# for tweet in tweepy.Cursor(api.search, q='#bmw', rpp=100).items(10):
#     msg = [tweet.text, tweet.source, tweet.source_url] 
#     msg = tuple(msg)                    
#     msgs.append(msg)

# df = pd.DataFrame(msgs)


import tweepy
import pandas as pd
import datetime
import os
from elasticsearch import Elasticsearch
es = Elasticsearch([{"host":'localhost',"port":'9200'}])


TWITTER_CONSUMER_KEY="ftZimOyZkpVFyKz06ura116Ci"
TWITTER_CONSUMER_SECRET="eaZUg0MAstAmciLb4tXtI6Xw3ganCEv2KnBRsxPQQuQruyT6SP"

MAX_TWEETS = 50000

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
api = tweepy.API(auth)
api = tweepy.API(auth,wait_on_rate_limit = True)
all_tweets=[]
df = pd.DataFrame(columns=['text', 'source', 'url'])
msgs = []
msg =[]
start_date = datetime.datetime(2021, 9, 14, 12, 00, 00)
end_date = datetime.datetime(2020, 1, 19, 13, 00, 00)

for tweet in tweepy.Cursor(api.search, q='#Ravens', rpp=100).items(MAX_TWEETS):
    all_data={
                "id":tweet.user.id,
                "tweet_id":tweet.id,
                "username": tweet.user.screen_name,
                "name":tweet.user.name,
                'freinds':api.get_user(tweet.user.id).friends_count,
                "created_at":tweet.user.created_at,
                "text":tweet.text,
                "source":tweet.source,
                "tweet_created_date":tweet.created_at,
                "tweet_url":"https://twitter.com/twitter/statuses/{}".format(tweet.id),
                "description": tweet.user.description,
                "location" :tweet.user.location,
                "following" : tweet.user.friends_count,
                "followers" : tweet.user.followers_count,
                "totaltweets" : tweet.user.statuses_count,
                "retweetcount" : tweet.retweet_count,
                "hashtags" : tweet.entities['hashtags']
            }
    all_tweets.append(all_data)
    es.index(index="trending_hashtags_tweets", doc_type='trendstweets', id=tweet.id,body=all_data, request_timeout=200)
print(all_tweets)