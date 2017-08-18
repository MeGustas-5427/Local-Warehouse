import re
import os
import sys
import pandas as pd
from textblob import TextBlob
from pyecharts import Pie
from langid.langid import LanguageIdentifier,model

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
"""
def main():
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) # 创建一个字典，用来转化无法识别的编码，即表情符号

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'].translate(non_bmp_map))
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'].translate(non_bmp_map))
"""

List = os.listdir("100 lastest tweets of the user")
identifier = LanguageIdentifier.from_modelstring(model,norm_probs = True)
Neutral_count, Negative_count, Positive_count = 0, 0, 0

for file in List:
    file = "100 lastest tweets of the user"+"//"+file
    if ".xlsx" in file:
        text_List = [text for text in list(pd.read_excel(file)["tweet"]) if identifier.classify(text)[0] == "en"]
        if len(text_List) == 0:
            print(file)
            continue # 如果推主的推文全都是非英语语种，则跳过
        tweets    = get_tweets(text_List)
        ptweets   = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        Positive  = 100*len(ptweets)/len(tweets)
        # print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

        ntweets  = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        Negative = 100*len(ntweets)/len(tweets)
        # print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

        Neutral  = 100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
        # print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

        result  = {Neutral:"Neutral", Negative:"Negative", Positive:"Positive"}
        result  = result[max([Positive, Negative, Neutral])]

        if   result == "Neutral" : Neutral_count  += 1
        elif result == "Negative": Negative_count += 1
        else                     : Positive_count += 1

print("Positive tweets count:",Positive_count)
print("Negative tweets count:",Negative_count)
print("Neutral  tweets count:",Neutral_count )

attr = ["positive", "negative", "neutral"]
v1 = [Positive_count, Negative_count, Neutral_count]
pie = Pie("Pie chart")
pie.add("", attr, v1, is_label_show=True)
pie.show_config()
pie.render(path="推主情感分析饼图.html")

