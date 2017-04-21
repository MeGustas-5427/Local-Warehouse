import xlrd,xlsxwriter,os
import easygui as eg

#=================【第一项步骤】=======================

Path1 = eg.fileopenbox('Please select file','open',default = '*.xlsx')
print(Path1)

#-(1)：【read xlsx】
ticker_dict ={}

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

#-(2)：【进行ticker名统计：出现次数、公司统计、公司出现日期收集】
    for each_rows in range(num,sheet.nrows):        
        value_list = sheet.row_values(each_rows)

        Ticker1 = value_list[Positon3].strip()
        company_name1 = value_list[Positon1].strip()
        
        ticker_dict.setdefault(Ticker1,{})

        ticker_dict[Ticker1].setdefault(company_name1,{})

        ticker_dict[Ticker1][company_name1].setdefault(value_list[Positon5],'')
                                                           
        ticker_dict[Ticker1][company_name1][value_list[Positon5]] = value_list[Positon6]

        if value_list[Positon2].strip() != '':
            Ticker2 = value_list[Positon4].strip()
            company_name2 = value_list[Positon2].strip()
            
            ticker_dict.setdefault(Ticker2,{})

            ticker_dict[Ticker2].setdefault(company_name2,{})

            ticker_dict[Ticker2][company_name2].setdefault(value_list[Positon5],'')
                                                           
            ticker_dict[Ticker2][company_name2][value_list[Positon5]] = value_list[Positon7]            
    '''
    ticker_dict = { ticker:{公司名字:{日期:BD文本,
                                      日期:BD文本,
                                      ...},
                            公司名字:{日期:BD文本,
                                      日期:BD文本,
                                      ...},
                            ...
                            }
                    ticker:{公司名字:{日期:BD文本,
                                      日期:BD文本,
                                      ...},
                            公司名字:{日期:BD文本,
                                      日期:BD文本,
                                      ...},
                            ...
                            }
                    }
    '''

ticker_list = ['Ticker\tNb of firms\t' + 'Name of firms\tTime\tBD\t' * 4 + '\n']

a_dict = {}
for ticker in ticker_dict.keys():    
    company_count = len(ticker_dict[ticker].keys())
    company_date_content = ''
         
    for company in ticker_dict[ticker].keys():
        date_num = min(ticker_dict[ticker][company].keys())
 
        date_tuple = xlrd.xldate_as_tuple(date_num,work_book.datemode)             # 将 42375.0 转化为 (2016,1,6,0,0,0)
        date_list = [date_tuple[0],date_tuple[1],date_tuple[2]]                    # 将 (2016,1,6,0,0,0) 转 [2016,1,6]
        date_str = '%d/%d/%d' % (date_tuple[0],date_tuple[1],date_tuple[2])
        content = ticker_dict[ticker][company][date_num]
        
        if ticker == "-" or ticker == "NA" or ticker == "N/A":
            a_dict.setdefault(ticker,[["Ticker","Nb of firm","Name of firm","Time","BD"],[ticker,company_count,"","",""]])
            a_dict[ticker].append(['','',company,date_str,content,])

        else:
            company_date_content += company + '\t' + date_str + '\t' + content + '\t'

    ticker_list.append(ticker + '\t' + str(company_count) + '\t' + company_date_content + '\n')


file_name = os.path.splitext(os.path.basename(Path1))[0]

with open('Ticker' + file_name + '.txt','w') as file:
    for i in ticker_list:
        file.write(i)


xlsx_Name = '3个特殊ticker统计.xlsx'
work_book = xlsxwriter.Workbook(xlsx_Name)

for each_sheet,row_list in a_dict.items():
    if each_sheet == "N/A":
        work_sheet = work_book.add_worksheet("N-A")
    else:
        work_sheet = work_book.add_worksheet(str(each_sheet))                                      
    for row_num,each_row in enumerate(row_list):    # (7)行数变化
        for col_num,value in enumerate(each_row):
            work_sheet.write(row_num,col_num,value)

work_book.close() 



    
