import re
import os
import sys
import pandas as pd
from textblob import TextBlob
from pyecharts import Pie

def clean_tweet(tweet):
    '''
    Apply regex to remove the URL and useless strings
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    Apply textblob to do sentiment analysis
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
 
def get_tweets(text_List):
    '''
    Obtain the ocntent of the tweet to do analysis
    '''
    tweets = []

    for text in text_List:
        parsed_tweet = {}
        parsed_tweet['text'] = text
        parsed_tweet['sentiment'] = get_tweet_sentiment(text)
        if parsed_tweet not in tweets: # 只保存其中一条（去重复）
            tweets.append(parsed_tweet)
    return tweets

frame = pd.read_excel("twitter_individual.xlsx")

tweets = [tweet for tweet in frame["tweet"]]
tweets    = get_tweets(tweets)
ptweets   = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
#Positive  = 100*len(ptweets)/len(tweets)
# print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

ntweets  = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
#Negative = 100*len(ntweets)/len(tweets)
# print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

Neutral  = 100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
# print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

attr = ["positive", "negative", "neutral"]
v1   = [len(ptweets),len(ntweets),len(tweets)-len(ptweets)-len(ntweets)]
pie = Pie("Pie chart")
pie.add("", attr, v1, is_label_show=True)
pie.show_config()
pie.render(path="搜索推文的情感分析饼图.html")

    
