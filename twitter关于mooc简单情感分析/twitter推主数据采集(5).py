import pandas as pd
import tweepy
import time
import sys
import os

consumer_key = "xV1p0neVdPfOtistJgeZJDHQP"  
consumer_secret = "fbv9Om0civOciKWa9ZtKyEESlKMtsiP7KHL5fzuWsByyG04fqk"  
access_token = "893980317341450240-CFNSZAkWATHnTYgdt2wjyK0PiedPrM7"  
access_token_secret = "kBc1ehA2kElMhoeihRVbJA17LnghuHd80d63RF0psQRLb"
# 创建认证对象
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
# 设置你的access token和access secret
auth.set_access_token(access_token, access_token_secret)  
# 传入auth参数，创建API对象
api = tweepy.API(auth)     

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) # 创建一个字典，用来转化无法识别的编码，即表情符号

twitter_move = pd.read_excel("twitter_individual.xlsx")
user_name = set(twitter_move.loc[:,"user name"])

file = "100 lastest tweets of the user"
os.mkdir(file)

for name in user_name:
    frame = pd.DataFrame(columns = ["tweet","other tags","words mentioned in the tweet","the ID of the words metioned in the tweet"])

    try:
        # 使用上面的参数，调用user_timeline函数
        results = api.user_timeline(id=name, count=100)
    except tweepy.TweepError as reason: 
        if reason.api_code in [34,50,63]:
            continue
        elif reason.api_code in [88]:
            print("please stop for 15 minutes") # 如果15分钟内，请求数据下载超过180次，则停15分钟
            print(api.rate_limit_status()['resources']['search']) # 打印限速时间范围内，还剩多少次
            time.sleep(60*15)
            try:
                results = api.user_timeline(id=name, count=100)
            except tweepy.error.TweepError as reason:
                if reason.api_code in [34,50,63]:
                    continue
        
    # 遍历所拉取的全部微博
    for num, tweet in enumerate(results):  
        # 打印存在微博对象中的text字段
        content = tweet.text # .translate(non_bmp_map) # 博文

        hashtags    = [i["text"]         for i in tweet.entities["hashtags"] if i["text"].lower() != "mooc"]
        screen_name = [i["screen_name"]  for i in tweet.entities["user_mentions"]] 
        screen_id   = [i["id_str"]       for i in tweet.entities["user_mentions"]]
        hashtags    = ",".join(hashtags)      # 除了mooc以外的其他标签
        screen_name = ",".join(screen_name)   # 推文提及词
        screen_id   = ",".join(screen_id)     # 推文提及词的ID标签

        frame.loc[num] = [content, hashtags, screen_name, screen_id]

    frame.to_excel(file+"//"+name+".xlsx")
    #print(name,end=" ")
