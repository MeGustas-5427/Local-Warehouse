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
            elif 'Announcement Date' == each_value[each_value.find('A'):each_value.rfind('e')+1]:
                item_Dict['Announcement Date'] = value_list.index(each_value)
                count += 1
            if count == 5:
                break
        if count == 5:
            break
    
    Positon1 = item_Dict['Acquiror Name']
    Positon2 = item_Dict['Target Name']
    Positon3 = item_Dict['Acquiror Ticker Symbol']
    Positon4 = item_Dict['Target Ticker Symbol']    
    Positon5 = item_Dict['Announcement Date']

#-(2)：【进行公司名统计：出现次数、ticker统计、公司出现日期收集】
    for each_rows in range(num,sheet.nrows):        
        value_list = sheet.row_values(each_rows)

        date_tuple = xlrd.xldate_as_tuple(value_list[Positon5],work_book.datemode) # 将 42375.0 转化为 (2016,1,6,0,0,0) 
        date_list = [date_tuple[0],date_tuple[1],date_tuple[2]]                    # 将 (2016,1,6,0,0,0) 转 [2016,1,6]
        
        company_name1 = value_list[Positon1].strip()
        
        company_dict.setdefault(company_name1,[set(),[],0])
        
        company_dict[company_name1][0].add(value_list[Positon3].strip())       
        company_dict[company_name1][1].append(date_list)      
        company_dict[company_name1][2] += 1

        if value_list[Positon2].strip() != '':
            company_name2 = value_list[Positon2].strip()
            
            company_dict.setdefault(company_name2,[set(),[],0])
            
            company_dict[company_name2][0].add(value_list[Positon4].strip())          
            company_dict[company_name2][1].append(date_list)         
            company_dict[company_name2][2] += 1

    '''
    company_dict = { 公司名字:【ticker集合,【[2016,1,6],[2017,9,26]...】,公司名字出现总次数】,
                     公司名字:【ticker集合,【公司名字出现日期的列表...】,公司名字出现总次数】,
                    }
    '''
file_name = os.path.splitext(os.path.basename(Path1))[0]
with open(file_name + '.txt','w') as file:
    file.write('Name of firms\tFrequency\tTicker\n')
    for company_name,List in company_dict.items():
        if company_name != '':
            Set,date_list,count = List
            if len(Set) > 1:
                print(company_name,Set)
            temp_date = ''
            for year,month,day in date_list:
                temp_date += '%d/%d/%d\t' % (year,month,day)
            file.write('%s\t%d\t%s\t%s\n' % (company_name,count,Set,temp_date))



#-(3)：

company_dict2 = {}
for company_name,List in company_dict.items():
    if company_name != '':
        Set,date_list,count = List
        company_dict2.setdefault(company_name,[Set,count,{}])
        for year,month,day in date_list:
            company_dict2[company_name][2].setdefault(year,0)
            company_dict2[company_name][2][year] += 1
'''
company_dict2 = { 公司名字:【ticker集合,公司名字出现总次数,{2015:2,2013:5,2017:1}】,
                  公司名字:【ticker集合,公司名字出现总次数,{2014:2,2016:5,2013:1}】, 
                 }
'''
            
year_list = [2013,2014,2015,2016,2017]

excel_list = [['Name of firms','Ticker','Frequency',2013,2014,2015,2016,207]]

for company_name,List in company_dict2.items():
    excel_temp_list = []
    for i in [company_name,List[0],List[1]]:
        excel_temp_list.append(i)        
    for year in year_list:
        excel_temp_list.append(List[2].get(year,0))
    excel_list.append(excel_temp_list)


with open(file_name + ' 2.txt','w') as file:
    for excel_temp_list in excel_list:
        temp = excel_temp_list
        file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7]))


#-(4)：【wirte xlsx】
company_2013 = [['2013','Ticker']]
company_2014 = [['2014','Ticker']]
company_2015 = [['2015','Ticker']]
company_2016 = [['2016','Ticker']]
company_2017 = [['2017','Ticker']]

for company_name,List in company_dict2.items():
    for year in year_list:
        if List[2].get(year,False) != False:
            if year == 2013:
                company_2013.append([company_name,List[0]])
                break
            elif year == 2014:
                company_2014.append([company_name,List[0]])
                break
            elif year == 2015:
                company_2015.append([company_name,List[0]])
                break
            elif year == 2016:
                company_2016.append([company_name,List[0]])
                break
            elif year == 2017:
                company_2017.append([company_name,List[0]])
                break

company_year = [company_2013,company_2014,company_2015,company_2016,company_2017]

xlsx_Name = '年份 ' + os.path.basename(Path1)

work_book = xlsxwriter.Workbook(xlsx_Name)

for each_year in company_year:
    work_sheet = work_book.add_worksheet(each_year[0][0])                                       
    for row_num,[company,ticker] in enumerate(each_year):    # (7)行数变化
        for col_num,value in enumerate([company,ticker]):
            if isinstance(value,set):
                value = str(value)
            work_sheet.write(row_num,col_num,value)

work_book.close()    


print('程序完成')
