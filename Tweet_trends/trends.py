import tweepy
from elasticsearch import Elasticsearch
es = Elasticsearch([{"host":'localhost',"port":'9200'}])

# TWITTER_ACCESS_TOKEN="1361217148614402052-sKZR5p2SEe7V8UlrlJePg5STKBAXWA"
# TWITTER_ACCESS_SECRET="FAWs3H2L26nVkuxVgz3sCJjAUgZk1t2mp3S6AcEomlwpx"
# TWITTER_CONSUMER_KEY="ftZimOyZkpVFyKz06ura116Ci"
# TWITTER_CONSUMER_SECRET="eaZUg0MAstAmciLb4tXtI6Xw3ganCEv2KnBRsxPQQuQruyT6SP"

# assign the values accordingly
consumer_key = "ftZimOyZkpVFyKz06ura116Ci"
consumer_secret = "eaZUg0MAstAmciLb4tXtI6Xw3ganCEv2KnBRsxPQQuQruyT6SP"
access_token = "1361217148614402052-sKZR5p2SEe7V8UlrlJePg5STKBAXWA"
access_token_secret = "FAWs3H2L26nVkuxVgz3sCJjAUgZk1t2mp3S6AcEomlwpx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  
# set access to user's access key and access secret 
auth.set_access_token(access_token, access_token_secret)
  
# calling the api 
api = tweepy.API(auth)
  
# fetching the trends
trends = api.trends_place(1)
  
# printing the information
  
for value in trends:
    for trend in value['trends']:
        data={
            'name':trend['name'],
            'url':trend['url'],
            'query':trend['query'],
            'tweet_volume':trend['tweet_volume']
        }
        es.index(index="trending_hashtags", doc_type='trends', body=data, request_timeout=200)

print("Trending Hashtags Added")