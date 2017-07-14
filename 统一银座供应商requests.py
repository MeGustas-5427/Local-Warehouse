from six.moves.html_parser import HTMLParser
import pandas as pd
import requests
import re

s = requests.session()

r = s.get("http://60.208.131.8/ui/CheckImg.aspx")
with open("img.jpg","wb") as img:
    img.write(r.content)

captcha = input("输入图片验证码数字：")
txtName = input("输入用户名：")
txtPassWord = input("输入密码：")

html1 = s.post("http://60.208.131.8/ui/login.aspx",
               data = {
                   "txtName":txtName,
                   "txtPassWord":txtPassWord,
                   "txtCode":captcha,
                   "ASPxButton1":"加载供应商",
                   "__VIEWSTATE":"/wEPDwUJNDUxNTI3NzIwD2QWAgIDD2QWBAILDxYCHgNzcmMFFy4uLy8uLi9VSVxDaGVja0ltZy5hc3B4ZAIND2QWAgIBD2QWAgIBDxBkZBYAZGQ="
                   },
                params = {"type":"tc"})

__VIEWSTATE = re.search('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />',html1.text).group(1)
s.post("http://60.208.131.8/ui/login.aspx",
               data = {
                    '__VIEWSTATE':__VIEWSTATE,
                    'txtName':txtName,
                    'txtPassWord':txtPassWord,
                    'txtCode':captcha,
                    'drpSupcd':txtName,
                    'bntLogin':'登录',
                   })

html2 = s.get("http://60.208.131.8/ui/Sale/WebSaleQueryList.aspx")
__VIEWSTATE = re.search('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />',html2.text).group(1)

print("""
请输入查询的日期
日期格式为xxxx-xx-xx
譬如：2017-07-12
""")
txtBeginDate = input("请输入查询的开始日期：")
txtEndDate   = input("请输入查询的结束日期：")
B = False
E = False
while True:
    if re.search('(201\d-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]))',txtBeginDate) is None:
        txtBeginDate = input("格式不正确，请重新输入查询的 <开始> 日期：")
    else:
        B = True
    if re.search('(201\d-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]))',txtEndDate) is None:
        txtEndDate   = input("格式不正确，请重新输入查询的 {结束} 日期：")
    else:
        E = True
    if B and E:
        break
    
html3 = s.post("http://60.208.131.8/ui/Sale/WebSaleQueryList.aspx",
               data = {
                "__VIEWSTATE":__VIEWSTATE,
                "HiddenField1":txtName,
                "txtGoods":"请输入商品条码或名称",
                "way":"rdoGoods",
                "txtBeginDate":txtBeginDate,
                "txtEndDate":txtEndDate,
                "btnSelect":"查询"})

model = '<th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">操作</th>'
columns = re.findall(model,html3.text)[0] # 获得表格的列名

model = '<td>(.+?)</td><td>(.+?)</td><td align="left">(.+?)</td><td align="left">(.+?)</td><td align="right">(.+?)</td><td>(.+?)</td><td align="right">(.+?)</td><td align="right">(.+?)</td><td>'
data_list = re.findall(model,html3.text) # 获得表格的结构数据

frame = pd.DataFrame(data_list,columns=columns)

model = '<a id="(.+?)" href="javascript:__doPostBack\(\'(.+?)\',\'\'\)">查看</a>'
__EVENTTARGET = re.findall(model,html3.text)
__VIEWSTATE   = re.search('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />',html3.text).group(1)

Dict = {}
Dict["总表"] = frame
for num,data in enumerate(data_list):
    s.post("http://60.208.131.8/ui/Sale/WebSaleQueryList.aspx",
           data = {"__EVENTTARGET":__EVENTTARGET[num][1],
                   "__VIEWSTATE":__VIEWSTATE,
                   "HiddenField1":txtName,
                   "txtGoods":"请输入商品条码或名称",
                   "way":"rdoGoods",
                   "txtBeginDate":txtBeginDate,
                   "txtEndDate":txtEndDate})

    MCD = data[1]
    MAM = HTMLParser().unescape(data[3])
    number,goods = MAM.split("]")
    url = "http://60.208.131.8/ui/Sale/WebSaleGoodsQueryDetails.aspx"
    html4 = s.get(url,params = {"MCD":MCD,"MAM":number+"]"+goods}).text
    
    model = '<th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th>'
    columns = re.findall(model,html4)[0] # 获得表格的列名

    model = '<td align="left">(.+?)</td><td align="right">(.+?)</td><td align="right">(.+?)</td><td align="right">(.+?)</td>'
    data_list = re.findall(model,html4) # 获得表格的结构数据

    frame = pd.DataFrame(data_list,columns=columns)
    
    page = int(re.search('第<font color=\'red\'><b>1</b></font>页／共(\d)页，每页显示100条',html4).group(1))
    if page > 1:
        __VIEWSTATE   = re.search('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)" />',html4).group(1)
        model = '<form name="form1" method="post" action="(.+?)" id="form1">'
        url_params = re.findall(model,html4)[0]
        
        for page_num in range(2,page+1):
            
            html5 = s.post(url = "http://60.208.131.8/ui/Sale/"+url_params,
                           data = {"__EVENTTARGET":"AspNetPager1",
                                   "__VIEWSTATE":__VIEWSTATE,
                                   "__EVENTARGUMENT":str(page_num),
                                   "HiddenField1":MCD,
                                   "HiddenField2":MAM})
            model = '<th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th><th scope="col">(.+?)</th>'
            columns = re.findall(model,html5.text)[0] # 获得表格的列名

            model = '<td align="left">(.+?)</td><td align="right">(.+?)</td><td align="right">(.+?)</td><td align="right">(.+?)</td>'
            data_list = re.findall(model,html5.text) # 获得表格的结构数据

            frame2 = pd.DataFrame(data_list,columns=columns)
            frame = pd.concat([frame,frame2])
        
    
    Dict[MCD] = frame

file = pd.ExcelWriter("统一银座供应商.xlsx")
for coding,frame in Dict.items():
    frame.to_excel(file, sheet_name = coding, index = False)
file.close()
print("程序结束")



