import pandas as pd
from pyecharts import Pie

twitter = pd.read_excel("twitter.xlsx")

# 根据 信息来源 中含有移动操作系统的推主判断为个人筛选出来
twitter["judge"] = pd.notnull(twitter["resource of information"].str.extract(r'(android|iphone|ipad)',expand=False))
twitter_move1    = twitter[twitter["judge"]] # 个人

# 下面也是可以的：
# judge = pd.notnull(twitter["resource of information"].str.extract(r'(android|iphone|ipad)',expand=False))
# twitter_move1 = twitter.loc[twitter.index.where(judge).dropna(),:]

# 根据 用户ID 自我介绍中含有mooc、MOOC、we are、we're、Our词的推主判断为平台筛选出来
twitter = twitter[twitter["judge"] == False] # twitter_website
test = twitter["self introduction of user"].str.extract(r"(mooc|MOOC|Mooc|we are|we're|Our|our|Online|online|Official)",expand=False)
twitter["judge"] = pd.notnull(test)
twitter_website1 = twitter[twitter["judge"]] # 平台

# 根据 推主名称中含有mooc|MOOC|Mooc|Online|online词的推主判断为平台筛选出来
twitter = twitter[twitter["judge"] == False]
test = twitter["user name"].str.extract(r"(mooc|MOOC|Mooc|Online|online|Official)",expand=False)
twitter["judge"] = pd.notnull(test)
twitter_website2 = twitter[twitter["judge"]] # 平台

twitter_move2 = twitter[twitter["judge"] == False]

twitter_website = pd.concat([twitter_website1,twitter_website2])
twitter_move    = pd.concat([twitter_move1   ,twitter_move2])

# user_name = set(twitter_move.loc[:,"推主名称"])
twitter_move.to_excel("twitter_individual.xlsx")


attr = ["individual", "platform"]
v2 = [len(twitter_move), len(twitter_website)]
pie = Pie("", title_pos='center', width=900)
pie.add("", attr, v2, is_label_show=True)
pie.show_config() 
pie.render("individual vs plafform.html")
