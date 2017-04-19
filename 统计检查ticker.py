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
            if 'name' == each_value[each_value.find('n'):each_value.rfind('e')+1]:
                item_Dict['name'] = value_list.index(each_value)
                count += 1
            elif 'Ticker' == each_value[each_value.find('T'):each_value.rfind('r')+1]:
                item_Dict['Ticker'] = value_list.index(each_value)
                count += 1
            if count == 2:
                break
        if count == 2:
            break

    Positon1 = item_Dict['name']
    Positon2 = item_Dict['Ticker']

#-(2)：【进行ticker名统计：出现次数、公司统计、公司出现日期收集】
    for each_rows in range(num,sheet.nrows):        
        value_list = sheet.row_values(each_rows)

        Ticker1 = value_list[Positon2].strip()
        company_name1 = value_list[Positon1].strip()
        
        ticker_dict.setdefault(Ticker1,[[],0])
      
        ticker_dict[Ticker1][0].append(company_name1)      
        ticker_dict[Ticker1][1] += 1


    '''
    ticker_dict = { ticker:【[公司名字，公司名字公司名字...],ticker名字出现总次数】,
                    ticker:【[公司名字，公司名字公司名字...],ticker名字出现总次数】,
                    }
    '''

file_name = os.path.splitext(os.path.basename(Path1))[0]

with open('Ticker' + file_name + '.txt','w') as file:
    file.write('Ticker\tFrequency\tName of firms\n')
    for ticker,List in ticker_dict.items():
        company_list,ticker_count = List
        company_name = ''
        for company in company_list:
            company_name += company + '\t'
        file.write('%s\t%d\t%s\n' % (ticker, ticker_count, company_name))





    
