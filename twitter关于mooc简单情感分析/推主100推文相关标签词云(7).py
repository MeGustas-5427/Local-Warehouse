import os
import pandas as pd
from pyecharts import WordCloud

List = os.listdir("100 lastest tweets of the user")

label_list = [label for file in List if ".xlsx" in "100 lastest tweets of the user//"+file
                    for labels in list(pd.read_excel("100 lastest tweets of the user//"+file)["other tags"]) if pd.notnull(labels)
                    for label in labels.split(",")]
              
label_list = [[i,label_list.count(i)] for i in set(label_list)]
frame = pd.DataFrame(label_list)
frame = frame.sort_values(by=1, ascending=False)

name  = list(frame.iloc[:,0])[:100]
value = list(frame.iloc[:,1])[:100]

wordcloud = WordCloud(width=1300, height=620)
wordcloud.add("", name, value, word_size_range=[20, 100])
wordcloud.show_config()
wordcloud.render("the wordcloud of the related tags of the 100 lastest tweets of the user.html")
