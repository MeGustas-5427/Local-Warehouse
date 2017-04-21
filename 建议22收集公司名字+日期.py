import xlrd,xlsxwriter,os
import easygui as eg

#=================【第一项步骤】=======================

Path1 = eg.fileopenbox('Please select file','open',default = '*.xlsx')
print(Path1)
#-(1)：【read xlsx】
company_dict ={}

work_book = xlrd.open_workbook(Path1)                  # (1)打开 文件
sheet_list = work_book.sheet_names()                   # (2)读取 工作表 名(全部)
for each_sheet in sheet_list:                          # (3)历遍 工作表 名
    sheet  = work_book.sheet_by_name(each_sheet)       # (4)读取 工作表 内容
    item_Dict = {}
    num = 0
    for each_rows in range(5):                         # (5)找出 两个目标列表
        count = 0
        num += 1
        value_list = sheet.row_values(each_rows)
        for each_value in value_list:
            each_value = str(each_value)
            if 'Acquiror Name' == each_value[each_value.find('A'):each_value.rfind('e')+1]:
                item_Dict['Acquiror Name'] = value_list.index(each_value)
                count += 1
            elif 'Target Name' == each_value[each_value.find('T'):each_value.rfind('e')+1]:
                item_Dict['Target Name'] = value_list.index(each_value)
                count += 1
            elif 'Acquiror Ticker Symbol' == each_value[each_value.find('A'):each_value.rfind('l')+1]:
                item_Dict['Acquiror Ticker Symbol'] = value_list.index(each_value)
                count += 1
            elif 'Target Ticker Symbol' == each_value[each_value.find('T'):each_value.rfind('l')+1]:
                item_Dict['Target Ticker Symbol'] = value_list.index(each_value)
                count += 1
            elif 'Acquiror Business Description' == each_value[each_value.find('A'):each_value.rfind('n')+1]:
                item_Dict['Acquiror Business Description'] = value_list.index(each_value)
                count += 1
            elif 'Target Business Description' == each_value[each_value.find('T'):each_value.rfind('n')+1]:
                item_Dict['Target Business Description'] = value_list.index(each_value)
                count += 1 
            elif 'Announcement Date' == each_value[each_value.find('A'):each_value.rfind('e')+1]:
                item_Dict['Announcement Date'] = value_list.index(each_value)
                count += 1
            if count == 7:
                break
        if count == 7:
            break
    
    Positon1 = item_Dict['Acquiror Name']
    Positon2 = item_Dict['Target Name']
    Positon3 = item_Dict['Acquiror Ticker Symbol']
    Positon4 = item_Dict['Target Ticker Symbol']    
    Positon5 = item_Dict['Announcement Date']
    Positon6 = item_Dict['Acquiror Business Description']
    Positon7 = item_Dict['Target Business Description']
    

#-(2)：【进行公司名统计：出现次数、ticker统计、公司出现日期收集】
    for each_rows in range(num,sheet.nrows):        
        value_list = sheet.row_values(each_rows)
     
        company_name1 = value_list[Positon1].strip()
        
        company_dict.setdefault(company_name1,[{},0])

        ATS = value_list[Positon3].strip()
        ABD = value_list[Positon6].strip()
        if company_dict[company_name1][0].get(value_list[Positon5],False) == False: # 对同一天出现多次只取第一次
            company_dict[company_name1][0][value_list[Positon5]] = [ATS,ABD]
        company_dict[company_name1][1] += 1

        if value_list[Positon2].strip() != '':
            company_name2 = value_list[Positon2].strip()
            
            company_dict.setdefault(company_name2,[{},0])

            TTS = value_list[Positon4].strip()
            TBD = value_list[Positon7].strip()
            if company_dict[company_name2][0].get(value_list[Positon5],False) == False: # 对同一天出现多次只取第一次
                company_dict[company_name2][0][value_list[Positon5]] = [TTS,TBD]         
            company_dict[company_name2][1] += 1

    '''
    company_dict = { 公司名字:【{42375.0:[ticker,原文],42305.0:[ticker2,原文]...},公司名字出现总次数】,
                     公司名字:【{日期的常数类型:[不同或相同的ticker,Business Description]...},公司名字出现总次数】,
                    }
    '''
file_name = os.path.splitext(os.path.basename(Path1))[0]


#-(3)：【wirte xlsx】
company_2013 = [['name','Ticker','日期','Business Description']]
company_2014 = [['name','Ticker','日期','Business Description']]
company_2015 = [['name','Ticker','日期','Business Description']]
company_2016 = [['name','Ticker','日期','Business Description']]
company_2017 = [['name','Ticker','日期','Business Description']]

for company_name,List in company_dict.items():
    
    date = min(List[0].keys())
    date_tuple = xlrd.xldate_as_tuple(date,work_book.datemode)                 # 将 42375.0 转化为 (2016,1,6,0,0,0)
    date_list = [date_tuple[0],date_tuple[1],date_tuple[2]]                    # 将 (2016,1,6,0,0,0) 转 [2016,1,6]
    date_str = '%d/%d/%d' % (date_tuple[0],date_tuple[1],date_tuple[2])
    
    if date_list[0] == 2013:
        company_2013.append([company_name, List[0][date][0], date_str, List[0][date][1]])

    elif date_list[0] == 2014:
        company_2014.append([company_name, List[0][date][0], date_str, List[0][date][1]])

    elif date_list[0] == 2015:
        company_2015.append([company_name, List[0][date][0], date_str, List[0][date][1]])

    elif date_list[0] == 2016:
        company_2016.append([company_name, List[0][date][0], date_str, List[0][date][1]])
 
    elif date_list[0] == 2017:
        company_2017.append([company_name, List[0][date][0], date_str, List[0][date][1]])


company_year = [company_2013,company_2014,company_2015,company_2016,company_2017]

xlsx_Name = '年份 ' + os.path.basename(Path1)

work_book = xlsxwriter.Workbook(xlsx_Name)

year_list = [2013,2014,2015,2016,2017]

for x,each_year in enumerate(company_year):
    work_sheet = work_book.add_worksheet(str(year_list[x]))                                       
    for row_num,[company,ticker,date,content] in enumerate(each_year):    # (7)行数变化
        for col_num,value in enumerate([company,ticker,date,content]):
            work_sheet.write(row_num,col_num,value)

work_book.close()    


print('程序完成')
