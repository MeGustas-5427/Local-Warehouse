import tweepy
import pandas as pd
import sys

consumer_key = "jH1xFLVT5KQkKsCtTl0fwiIft"  
consumer_secret = "qwVSUuk3IXt3qyj8qg36Hb6VLGOeBASBaWuhsqAIhWPYd4n0te"  
access_token = "893980317341450240-jpPtlhizf5Kdfvv0nI6UlPzLhHb6dGa"  
access_token_secret = "GB3XSDi7DVSlRy797V0R1M7mFPNpvtxql0ASjOTiS0KtU"
# 以上4行是开发者账号的账号名和密码
# 创建认证对象
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
# 设置你的access token和access secret
auth.set_access_token(access_token, access_token_secret)  
# 传入auth参数，创建API对象
api = tweepy.API(auth)   

# 使用API对象获取你的时间轴上的微博，并把结果存在一个叫做public_tweets的变量中
# public_tweets = api.home_timeline()  

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) # 创建一个字典，用来转化无法识别的编码，即表情符号

#frame = pd.DataFrame(columns=["创建推文的时间","推主名称","推主地区","信息来源","博文",
                              #"转发次数","点赞次数","推文链接","其他标签","推文提及词","推文提及词的ID标签",
                              #"用户ID 自我介绍","用户ID 点赞次数","用户ID 关注者数量","用户ID 正在关注数量",
                             # "用户ID 推文数量","用户ID 创建时间","用户ID 创建ID所在时区","世界标准时间 抵消"]) # 创建一个表格

frame = pd.DataFrame(columns=["creation time of the tweet","user name","region of the tweet","resource of information","tweet",
                              "the link of tweet","other tags","words mentioned in the tweet","the ID of the words metioned in the tweet",
                              "self introduction of user","creation time of the user","region of the account","global standard time offset"])

frame_history = pd.read_excel("twitter.xlsx")
date_history  = list(frame_history["creation time of the tweet"])
# q是搜索词参数，result_type只有三种选择：recent：近7天数据，mixed：Include both popular and real time results in the response，popular ：return only the most popular results in the response
twitter = tweepy.Cursor(api.search, q="#mooc", count=100, result_type="recent", 
                      include_entities=True, lang="en").items() # count上限是100
# twitter为搜索设置
count = 0
#count = len(frame_history)
while 1:
   try:
      tweet = next(twitter)  # 执行搜索并返回搜索结果 
   except tweepy.TweepError: # 如果15分钟内，请求数据下载超过180次，则停15分钟
      print("please stop for 15 minutes")
      time.sleep(60*15)
      continue
   except StopIteration:     # 如果数据下载完成，则自动跳出循环 
      break

   date    = tweet.created_at                  # 创建推文的时间
   if date in date_history:
      break
   username= tweet.user.screen_name            # 推主名称
   locat   = tweet.user.location               # 推主地区
   source  = tweet.source_url                  # 信息来源
   content = tweet.text.translate(non_bmp_map) # 博文
   
   try:link = tweet.entities["urls"][0]["expanded_url"] # 博文链接
   except: link = ""

   hashtags    = [i["text"]         for i in tweet.entities["hashtags"] if i["text"].lower() != "mooc"]
   screen_name = [i["screen_name"]  for i in tweet.entities["user_mentions"]] 
   screen_id   = [i["id_str"]       for i in tweet.entities["user_mentions"]]

   hashtags    = ",".join(hashtags)      # 除了mooc以外的其他标签
   screen_name = ",".join(screen_name)   # 推文提及词
   screen_id   = ",".join(screen_id)     # 推文提及词的ID标签
   
   descrip = tweet.user.description      # 用户ID 自我介绍
   created = tweet.user.created_at       # 用户ID 创建时间
   t_zone  = tweet.user.time_zone        # 用户ID 创建ID所在时区
   UTC_offset = tweet.user.utc_offset    # 世界标准时间 抵消

   frame.loc[count] = [date, username, locat, source, content,
                       link, hashtags, screen_name, screen_id,
                       descrip, created, t_zone, UTC_offset] # 把数据写入表格
   count += 1
   
print("We have collected",count,"slices of information")                       
print(api.rate_limit_status()['resources']['search']) # 打印限速时间范围内，还剩多少次
frame = pd.concat([frame,pd.read_excel("twitter.xlsx")])
frame.to_excel("twitter3.xlsx",index=False)   # 输出表格
