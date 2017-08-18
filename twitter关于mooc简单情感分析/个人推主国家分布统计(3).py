import pandas as pd
from pyecharts import Pie

Developed_Countries = pd.read_excel("List of Developed Countries.xlsx")["Developed Countries"]
frame = pd.read_excel("twitter_individual.xlsx",usecols=[1,2])
frame = frame.dropna()
frame["region of the tweet"] = frame["region of the tweet"].str.strip()
frame["user name"] = frame["user name"].str.strip()
frame = frame.drop_duplicates("user name")

contry_dict = pd.read_excel("region dictionary.xlsx")
contry_dict["city"] = contry_dict["city"].str.strip()
contry_dict = contry_dict.drop_duplicates()
contry_dict = contry_dict.set_index("city")

#data = [local for local in frame["region of the tweet"] if local not in contry_dict["new area"]]

data = [contry_dict.ix[local]["new area"] for local in frame["region of the tweet"]]
Deve_Coun_Count = [1 for country in data if country in list(Developed_Countries)]
series = pd.Series(data)
a = series.value_counts()
country = series.value_counts().index
count   = series.value_counts().values

pie = Pie("",width=2000,height=1000)
pie.add("发达国家与发展中国家", ["发达国家","发展中国家"],
        [len(Deve_Coun_Count),len(data)-len(Deve_Coun_Count)-data.count("Unknown")],
         is_label_show=True,center=[20, 55])
pie.add("推主的国家分布", country, count, is_label_show=True,center=[70, 55])
pie.show_config()
pie.render("Summary of the region of individual tweeters.html")
