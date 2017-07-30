from selenium import webdriver
import pandas as pd

frame = pd.DataFrame(columns = ["Course","Link"])
url = "https://www.youtube.com/watch?v=X4QQNEhKRzI&list=PLil-R4o6jmGibE_uaJMjBV1UJi3MwgDJ0"

browser = webdriver.Chrome("F:\chromedriver.exe")
browser.set_page_load_timeout(60)
browser.get(url)

li_list = browser.find_elements_by_css_selector("#playlist-autoscroll-list > li")

def result():                
    for li in li_list:
        course = li.find_element_by_tag_name("h4").text
        link   = li.find_element_by_tag_name("a").get_attribute("href")
        print(course)
        print(link)
        print("=================")
        yield [course,"youtube-dl -f 22 "+link]
r = result()
for count in range(1,1+len(li_list)):
    frame.loc[count] = next(r)

frame.to_excel("台湾大学 统计学.xlsx",sheet_name = "2013年10月25日发布")
browser.quit()
