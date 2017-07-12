import asyncio
import aiohttp
import requests
from lxml import etree
import pandas as pd

async def get_http(link):
    async with aiohttp.request("GET",link,headers=headers) as response:
        frame = pd.DataFrame(columns = ["日期",
                                "最高气温",
                                "最低气温",
                                "天气",
                                "风向",
                                "风力"])
        
        text = await response.text()
        
        for ul in etree.HTML(text).xpath('//div[@class="tqtongji2"]/ul')[1:]:
            date       = [ul.xpath('.//a/text()')[0]    if ul.xpath('.//a/text()')    else ul.xpath('./li[1]/text()')[0]][0]
            highest    = [ul.xpath('./li[2]/text()')[0] if ul.xpath('./li[2]/text()') else ""][0]
            lowest     = [ul.xpath('./li[3]/text()')[0] if ul.xpath('./li[3]/text()') else ""][0]
            weather    = [ul.xpath('./li[4]/text()')[0] if ul.xpath('./li[4]/text()') else ""][0]
            direction  = [ul.xpath('./li[5]/text()')[0] if ul.xpath('./li[5]/text()') else ""][0]
            wind_power = [ul.xpath('./li[6]/text()')[0] if ul.xpath('./li[6]/text()') else ""][0]
            data = [date, highest, lowest, weather, direction, wind_power]
            temp_frame = pd.DataFrame([data], columns = ["日期",
                                                       "最高气温",
                                                       "最低气温",
                                                       "天气",
                                                       "风向",
                                                       "风力"])
            frame = pd.concat([frame,temp_frame])
        return frame

if __name__ == "__main__":
    headers = {
        "uesr_agent":'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }

    r = requests.get('http://lishi.tianqi.com/beijing/index.html',headers=headers)

    Link_List = etree.HTML(r.text).xpath('//div[@class="tqtongji1"]//a/@href')
        
    Event_Loop = asyncio.get_event_loop()
    Tasks = [get_http(link) for link in Link_List]
    Frame_List = Event_Loop.run_until_complete(asyncio.gather(*Tasks))
    Event_Loop.close()

    Frame = pd.concat(Frame_List)
    
    Frame.to_excel("北京历史天气.xlsx")
