import pandas as pd
import datetime
import re
import numpy as np
from io import StringIO
from business_calendar import Calendar, MO, TU, WE, TH, FR, SA, SU
# pd.set_option('mode.chained_assignment',None)

# 生成地区对应国家字典
print("生成地区对应国家字典")
City_Country = pd.read_excel("country0810.xlsx")
City_Country = City_Country.drop_duplicates()
City_Country = City_Country.set_index("Work Location City")

# 生成国家对应假期字典 { 国家：[所有节假日] }
print("生成国家对应假期字典 { 国家：[所有节假日] }")
Holiday = pd.read_csv("Holiday.csv",usecols=[0,5,6],encoding = "latin1")
Holiday["Start Date"] = pd.to_datetime(Holiday["Start Date"],infer_datetime_format=True)
Holiday["End Date"]   = pd.to_datetime(Holiday["End Date"]  ,infer_datetime_format=True)
Holiday = Holiday.drop_duplicates()
Holiday = Holiday.dropna()
Holiday_group = Holiday.groupby("Country")

Holiday_Dict = {}
for Country,frame in Holiday_group:
    date_list = []
    for num in frame.index:
        a = pd.date_range(frame.loc[num,"Start Date"],frame.loc[num,"End Date"],freg = "D")
        a = list(a.astype(str))
        date_list += a
    Holiday_Dict[Country] = date_list

# 生成员工请假字典
print("生成员工请假字典")
Timeoff = pd.read_csv("Timeoff Table 20140101 20170714 2017-07-14 12_07 PDT.csv",usecols=[0,1,2,4])
Timeoff = Timeoff[Timeoff["Status"] == "Approved"]
Timeoff["Time Off Date"] = pd.to_datetime(Timeoff["Time Off Date"],infer_datetime_format=True)
Timeoff['EmployeeID'] = Timeoff['EmployeeID'].astype(str)
Timeoff = Timeoff.dropna()
Timeoff_group = Timeoff.groupby("EmployeeID")

Timeoff_Dict = {}
for EmployeeID,frame in Timeoff_group:
    frame.is_copy = False
    frame["Hours"] = frame["Hours"].astype(int) # 把Hours列转化为整数类型，便于数学统计
    date_serise = frame.groupby("Time Off Date")["Hours"].aggregate(sum) # 统计
    date_serise = date_serise[date_serise > 0]
    Timeoff_Dict[EmployeeID] = list(date_serise.index.astype(str))
    
# 生成员工打卡表的休假时间统计
print("生成员工打卡表的休假时间统计")
frame = pd.read_csv("securitydata111.csv")
frame['CardHolderID'] = frame['CardHolderID'].astype(str)
Worker_Info = pd.read_csv("WorkerInfo.csv")
Worker_Info['Employee ID'] = Worker_Info['Employee ID'].astype(str)
CardHolderID = list(set(Worker_Info['Employee ID']) & set(frame['CardHolderID']))
frame = frame[frame["CardHolderID"].isin(CardHolderID)]

# """ 临时代码"""
frame = frame[frame["city"].isin(list(City_Country.index))]
# """ 临时代码"""
judge = pd.notnull(frame["BadgeDate"].str.extract(r'(^\d{1,2}/\d{1,2}/\d{4})',expand = False)) # 把以xx/xx/xxxx开头的日期匹配出来
frame = frame.loc[frame.index.where(judge).dropna(),:]                     # 删除不是以以xx/xx/xxxx开头的行
frame["BadgeDate"] = frame["BadgeDate"].str.split(' ')                     # 把日期 转换为 [02/04/2016, , 5:38AM] 这样的格式
frame["BadgeDate"] = frame["BadgeDate"].map(lambda x: x[0])                # [02/04/2016, , 5:38AM] 这样的格式里面的02/04/2016这种内容提取出来
frame = frame.set_index("city")                                            # 将city列 设置为索引

frame["Exportdate"]   = pd.to_datetime(frame["Exportdate"]  ,infer_datetime_format=True) # Exportdate列 字符串类型日期 转换为 日期类型
frame = frame.sort_values(by = "Exportdate")  # 根据 Exportdate列 进行排序

frame_group = frame.groupby('CardHolderID')   # 根据 CardHolderID列 进行分组
print("一共%d组" % (len(dict(list(frame_group)))))
count = 1
frame_list = []
Employee_Workday_Count = pd.DataFrame(columns = ["Employee Workday Count"]) # 创建一个表，用来收集每个员工的打卡总天数
for ID,frame in frame_group:  # ID = CardHolderID，即员工ID ， frame是该员工的全部打打记录表
    print(count,end = " ")
    count += 1
    Employee_Workday_Count.loc[ID,"Employee Workday Count"] = len(frame) # 统计每个员工的打卡总天数
    frame = frame.drop_duplicates("BadgeDate")                           # 如果 BadgeDate列 有重复日期，去重复
    frame.is_copy = False
    frame.loc[:,"BadgeDate"] = frame.loc[:,"BadgeDate"].map(lambda x: (x.split("/")[2],x.split("/")[0],x.split("/")[1])) # 把02/04/2016转为["2016","02","04"]
    frame.loc[:,"BadgeDate"] = frame.loc[:,"BadgeDate"].map(lambda x: (int(x[0]),int(x[1]),int(x[2])))                   # 把["2016","02","04"]转为[(2016,2,4)
    frame.loc[:,"BadgeDate2"] = list(frame.loc[:,"BadgeDate"][1:])+[""]  # 这个难以文字描述，我语音描述吧
    frame = frame.iloc[:-1] # 这个难以文字描述，我语音描述吧
    Holiday_Count0 = []
    Holiday_Count1 = []
    Holiday_Count2 = []
    Holiday_Count3 = []
    Holiday_Count4 = []
    a              = []
    b              = []
    if ID in Timeoff_Dict.keys():
        Timeoff_list = Timeoff_Dict[ID] # 把员工ID对应的请教日期列表找出来
    else:
        Timeoff_list = []               # 如果找不到该员工ID的请教日期列表，则把该员工ID的请教列表设置为空
    
    for num,city in enumerate(frame.index):
        Country = City_Country.loc[city.strip('"'),'Work Location Country'] # 找出城市对应的国家
        Holiday = Holiday_Dict[Country]                                     # 找出国家对应的假日日期列表
        
        year1, month1, day1 = frame.iloc[num]["BadgeDate"]   # year=2016，month=2， day=4
        year2, month2, day2 = frame.iloc[num]["BadgeDate2"]

        date1 = datetime.datetime(year1, month1, day1)       # 把# year month day 转为为datatime类型
        date2 = datetime.datetime(year2, month2, day2)
        
        cal0 = Calendar()
        cal1 = Calendar(workdays =[SA,SU])
        cal2 = Calendar(workdays =[MO, TU, WE, TH, FR],holidays = ["2010-01-01","2020-01-01"]+Holiday+Timeoff_list)
        cal3 = Calendar(workdays =[MO, TU, WE, TH, FR, SA, SU],holidays = ["2010-01-01","2020-01-01"]+Holiday)
        cal4 = Calendar(workdays =[MO, TU, WE, TH, FR, SA, SU],holidays = ["2010-01-01","2020-01-01"]+Timeoff_list)  

        bsday0 = int(str(date2-date1).split(" ")[0]) - 1 # 打卡间隔天数
        
        date2  = date2 + datetime.timedelta(days = -1)   # 减去一天
        bsday1 = cal1.busdaycount(date1, date2)          # 打卡间隔天数的周六日天数
        bsday2 = cal2.busdaycount(date1, date2)          # 打卡间隔存在的休假日天数
        bsday3 = bsday0 - cal3.busdaycount(date1, date2) # 打卡间隔存在的节假日天数
        bsday4 = bsday0 - cal4.busdaycount(date1, date2) # 打卡间隔存在的请假日天数

        _a = bsday0 - bsday1
        _b = bsday1 - bsday2
        
        Holiday_Count0.append(bsday0)
        Holiday_Count1.append(bsday1)
        Holiday_Count2.append(bsday2)
        Holiday_Count3.append(bsday3)
        Holiday_Count4.append(bsday4)
        a.append(_a)
        b.append(_b)
    
    frame["Holiday Count0"] = Holiday_Count0
    frame["Holiday Count1"] = Holiday_Count1
    frame["Holiday Count2"] = Holiday_Count2
    frame["Holiday Count3"] = Holiday_Count3
    frame["Holiday Count4"] = Holiday_Count4
    frame["a"] = a
    frame["b"] = b
    frame_list.append(frame)
print("测试成功")

frame = pd.concat(frame_list)
frame.to_csv("test.csv")

# 生成员工休假时间对应的经理、部门统计
print("生成员工休假时间对应的经理、部门统计")
Worker_Info = pd.read_csv("WorkerInfo.csv")
Worker_Info['Employee ID'] = Worker_Info['Employee ID'].astype(str)      # 把ID列的员工ID转为字符串类型
Worker_Info = Worker_Info[Worker_Info['Employee ID'].isin(CardHolderID)] # 保留有用的ID
Worker_Info = Worker_Info.set_index('Employee ID')                       # 把员工ID设置为索引

Manager_Len  = len(set(Worker_Info["Manager Employee ID"].values))       # 统计经理ID的数量
Division_Len = len(set(Worker_Info["Supervisory Org Division"].values))  # 统计部门的数量
Manager  = list(set(Worker_Info["Manager Employee ID"].values))          # 把不重复的经理ID罗列出来，成为列表 [经理ID,经理ID,....]
Division = list(set(Worker_Info["Supervisory Org Division"].values))     # 把不重复的部门  罗列出来，成为列表 [部门A, 部门B, ....]
Manager_Frame  = pd.DataFrame(index = Manager ,columns = ['Holiday Count0','Holiday Count1','Holiday Count2','Holiday Count3','Holiday Count4','Employee Workday Count'])# 经理统计表
Division_Frame = pd.DataFrame(index = Division,columns = ['Holiday Count0','Holiday Count1','Holiday Count2','Holiday Count3','Holiday Count4','Employee Workday Count'])# 部门统计表

Manager_Frame.loc[:,:]  = 0 # 预先格式化为数字类型 0，便于下面统计时候进行加法计算
Division_Frame.loc[:,:] = 0 # 预先格式化为数字类型 0，便于下面统计时候进行加法计算
frame = frame.set_index("CardHolderID") # 把 员工ID 设置为索引列
for ID in set(frame.index): 
    Manager_ID = Worker_Info.loc[ID,'Manager Employee ID']     # 根据员工ID，找到对应的经理ID
    Division   = Worker_Info.loc[ID,'Supervisory Org Division']# 根据员工ID，找到对应的部门
    
    Holiday_Count0 = frame.loc[ID,'Holiday Count0'].sum()
    Holiday_Count1 = frame.loc[ID,'Holiday Count1'].sum()
    Holiday_Count2 = frame.loc[ID,'Holiday Count2'].sum()
    Holiday_Count3 = frame.loc[ID,'Holiday Count3'].sum()
    Holiday_Count4 = frame.loc[ID,'Holiday Count4'].sum()

    Manager_Frame.loc[Manager_ID,'Holiday Count0'] += Holiday_Count0
    Manager_Frame.loc[Manager_ID,'Holiday Count1'] += Holiday_Count1
    Manager_Frame.loc[Manager_ID,'Holiday Count2'] += Holiday_Count2
    Manager_Frame.loc[Manager_ID,'Holiday Count3'] += Holiday_Count3
    Manager_Frame.loc[Manager_ID,'Holiday Count4'] += Holiday_Count4
    
    Division_Frame.loc[Division,'Holiday Count0']  += Holiday_Count0
    Division_Frame.loc[Division,'Holiday Count1']  += Holiday_Count1
    Division_Frame.loc[Division,'Holiday Count2']  += Holiday_Count2
    Division_Frame.loc[Division,'Holiday Count3']  += Holiday_Count3
    Division_Frame.loc[Division,'Holiday Count4']  += Holiday_Count4

    Manager_Frame.loc[Manager_ID,'Employee Workday Count'] += Employee_Workday_Count.loc[ID,"Employee Workday Count"]
    Division_Frame.loc[Division,'Employee Workday Count']  += Employee_Workday_Count.loc[ID,"Employee Workday Count"]
    
Manager_Frame.to_csv("Manager Employee ID.csv")
Division_Frame.to_csv("Supervisory Org Division.csv")

