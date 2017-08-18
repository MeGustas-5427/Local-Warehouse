import pandas as pd
from pyecharts import WordCloud

frame = pd.read_excel("twitter_individual.xlsx",usecols=[6]).dropna()
label_list = [label for labels in frame.iloc[:,0] for label in labels.split(",")]
label_list = [[i,label_list.count(i)] for i in set(label_list)]
frame = pd.DataFrame(label_list)
frame = frame.sort_values(by=1, ascending=False)

name  = list(frame.iloc[:,0])[:100]
value = list(frame.iloc[:,1])[:100]

wordcloud = WordCloud(width=1300, height=620)
wordcloud.add("", name, value, word_size_range=[20, 100])
wordcloud.show_config()
wordcloud.render("wordcloud of related hashtags.html")
