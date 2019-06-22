# -*- coding: utf-8 -*-
import requests
from lxml import html
import math
import os
import time
from urllib.parse import quote
url='http://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=4&bidSort=&buyerName=&projectId=&pinMu=&bidType=7&dbselect=bidx&kw=&start_time=2018%3A12%3A22&end_time=2019%3A06%3A22&timeType=5&displayZone=&zoneId=&pppStatus=0&agentName=' #需要爬数据的网址
page=requests.get(url,timeout=30,headers={'user-agent': 'Mozilla/5.0'})

tree=html.fromstring(page.text)
# result=tree.xpath('//p[@style="float:left"]/span[2]/text()')
# result=tree.xpath('/html/body/div[5]/div[1]/div/p[1]/span[2]/text()')
# print (result)
# /html/body/div[5]/div[1]/div/p[1]/span[2]
# /html/body/div[5]/div[1]/div/p[1]/span[0]

year=[2019,2018,2017,2016,2015,2014,2013]

def getYearInformation(originurl):
    try:
        with open('result.txt','r',encoding="utf-8") as f:
            content = f.readlines()
        datas = []
        for i in range(len(content)):
            # print(content[i])
            data = ""
            kw1 = content[i].replace("\n","")
            kw1 = quote(kw1)
            kw2 = '电信'
            kw2 = kw1 + '+'+quote(kw2)

            newUrl1 = originurl.replace("kw=","kw="+kw1)
            newUrl2 = originurl.replace("kw=","kw="+kw2)
            # newUrl1 = url
            page1 = requests.get(newUrl1, timeout=30, headers={'user-agent': 'Mozilla/5.0'})
            tree1 = html.fromstring(page1.text)
            num1 = tree1.xpath('//p[@style="float:left"]/span[2]/text()')
            # print(num1)
            page2 = requests.get(newUrl2, timeout=30, headers={'user-agent': 'Mozilla/5.0'})
            tree2 = html.fromstring(page2.text)
            num2 = tree2.xpath('//p[@style="float:left"]/span[2]/text()')
            # print
            num3 = float(num2[0])/float(num1[0])
            if num3>0.05:
                data = content[i].replace("\n","") +" "+ num1[0]+ " "+ num2[0]+ " "+str(num3)[:6]+'\n'
                datas.append(data)
            with open ("nb2.txt","w") as f:
                for i in range(len(datas)):
                    f.writelines(datas[i])

            print(i)
    except:
        print("connect error")
        time.sleep(3)
        # pagenumber = math.ceil(int(num[0]) / 20)
        # for i in range(1, pagenumber + 1):
        #     print("begin page" + str(i) + '/' + str(pagenumber))
        #     tmpUrl = originurl.replace("page_index=1", "page_index=" + str(i))
        #     href_list, information_list = getPageHref(tmpUrl)
        #     for h in range(len(href_list)):
        #         getPageInformation(href_list[h], information_list[h])
        #     print("end page" + str(i) + '/' + str(pagenumber))

    # print("connect error")
    # time.sleep(3)

def getPageHref(pageurl):
    try:
        page = requests.get(pageurl,timeout=30,headers={'user-agent': 'Mozilla/5.0'})
        tree = html.fromstring(page.text)
        result = tree.xpath('//ul[@class="vT-srch-result-list-bid"]//li/a/@href')
        infomation = tree.xpath('//ul[@class="vT-srch-result-list-bid"]//li/span/text()')
        return result, infomation
    except:
        print("connect error")
        time.sleep(3)


def getPageInformation(hrefurl,information):
    try:
        page = requests.get(hrefurl,timeout=30,headers={'user-agent': 'Mozilla/5.0'})
        page.encoding='utf-8'
        tree = html.fromstring(page.text)
        title = tree.xpath('//div[@class="vF_detail_header" or @class="vT_detail_header"]//h2[@class="tc"]/text()')
        title[0]=title[0].replace("/","")
        title[0]=title[0].replace('\"',"")
        content = tree.xpath('//div[@class="vF_detail_main" or @class="vT_detail_main"]//text()')
        # abstract = tree.xpath('//div[@class="table" or @class="vT_detail_content" or @class="vT_detail_content w760c"]//td/text()')
        # content = tree.xpath('//div[@class="vF_detail_content" or @class="vT_detail_content" or @class="vT_detail_content w760c"]//span/text()')
        # content2 = tree.xpath('//div[@class="vF_detail_content" or @class="vT_detail_content" or @class="vT_detail_content w760c"]//p/text()')
        # table = tree.xpath('//div[@class="vF_detail_content" or @class="vT_detail_content" or @class="vT_detail_content w760c"]/table//table//text()')
    except Exception as msg:
        print("connect error of page information")
        print("error:",msg)
        time.sleep(3)
    global i
    try:

        with open('./'+str(year[i])+'/'+title[0]+'.txt','w',encoding="utf-8") as f:
            f.write(information)
            # for t in range(len(abstract)):
            #     f.write(abstract[t])
            for t in range(len(content)):
                f.write(content[t])
            # for t in range(len(content2)):
            #     f.write(content2[t])
            # for t in range(len(table)):
            #     f.write(table[t])
    except Exception as msg:
        print("file error")
        print("error:",msg)

# i=2
# while i<6:
#     newUrl = url.replace("start_time=2018","start_time="+str(year[i+1]))
#     newUrl = newUrl.replace("end_time=2019","end_time="+str(year[i]))
#     print("begin",year[i])
#     if(os.path.exists(str(year[i]))==False):
#         os.mkdir(str(year[i]))
#         getYearInformation(newUrl)
#     else:
#         getYearInformation(newUrl)
#     print("finish",year[i])
#     i+=1
# i=5
getYearInformation(url)