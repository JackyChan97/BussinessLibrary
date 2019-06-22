from urllib.parse import quote
import urllib.request
from bs4 import  BeautifulSoup
import requests
from lxml import html
import time
from index.models import  Project
import math

KEY_WORD = '电信'
NUMBER_PAGE = 1 #爬虫页数

def encode_kw(kw):
    return quote(kw)


def update1():
    titles = Project.objects.get(sourceId=1)
    for title in titles:#titles 取自数据库
        title = title[:-8]
        enc_title = encode_kw(title)
        url = "http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=7&dbselect=bidx&kw=%s" % enc_title + "&start_time=2019%3A05%3A21&end_time=2019%3A06%3A21&timeType=3&displayZone=&zoneId=&pppStatus=0&agentName="
        _, _, title_list = getPageHref(url)
        if len(title_list) != 0:
            #删除项目信息
            title.delete()
            print("已中标，删除")



def spider1(page_n,kw):
    datas = []
    kw = encode_kw(kw)
    url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=1&dbselect=bidx&kw=%s' % kw + '&start_time=2019%3A05%3A21&end_time=2019%3A06%3A21&timeType=3&displayZone=&zoneId=&pppStatus=0&agentName=' # 需要爬数据的网址

    # try:
    #     last_title = LastProject.objects.get(sourceId=1).name
    # except:
    #     last_title = '-1'
    repeated = False
    for i in range(1, page_n + 1):
        tmpUrl = url.replace("page_index=1", "page_index=" + str(i))
        href_list, information_list,title_list = getPageHref(tmpUrl)
        for j in range(0,len(href_list)):
            data = []
            title = title_list[j].replace(' ','').replace('\r','').replace('\n','')
            date = information_list[5 * j][0:10]
            date = date.replace('.','-')
            link = href_list[j]

            # if title == last_title:
            #     repeated = True
            #     break

            data.append(title)
            data.append(date)
            data.append(link)
            data.append(1)
            datas.append(data)
        # if repeated == True:
        #     print("已经重复")
        #     break
    return datas

def getPageHref(pageurl):
    try:
        page = requests.get(pageurl, timeout=30, headers={'user-agent': 'Mozilla/5.0'})
        tree = html.fromstring(page.text)
        result = tree.xpath('//ul[@class="vT-srch-result-list-bid"]//li/a/@href')
        infomation = tree.xpath('//ul[@class="vT-srch-result-list-bid"]//li/span/text()')
        title = tree.xpath('//ul[@class="vT-srch-result-list-bid"]//li/a/text()')
        return result, infomation,title
    except:
        print("connect error")
        time.sleep(3)



def update2():
    titles = Project.objects.get(sourceId=2)
    for title in titles:#titles 取自数据库
        title = title[:-8]
        formdata = {'fullText': title,
                    'pubDate': '',
                    'infoClassCodes': '0108',
                    'normIndustry': '',
                    'zoneCode': '',
                    'fundSourceCodes': '',
                    'poClass': 'BidResult',
                    'rangeType': 2,
                    'currentPage': 1}
        r = requests.post('http://www.chinabidding.com/search/proj.htm', data=formdata)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup)

        links = soup.find_all(attrs={"class": "as-pager-item"})
        if len(links) != 0:
            #删除项目信息
            title.delete()
            print("已中标，删除")


def spider2(page_n,kw ='电信'):
    #http://www.chinabidding.com/search/proj.htm
    datas = []
    for i in range(1,page_n+1):
        # print("page %i" % i + " spiding")
        formdata = {'fullText': '电信',
                    'pubDate': '',
                    'infoClassCodes': '0105',
                    'normIndustry': '',
                    'zoneCode': '',
                    'fundSourceCodes': '',
                    'poClass': 'BidNotice',
                    'rangeType': 2,
                    'currentPage': 1}
        r = requests.post('http://www.chinabidding.com/search/proj.htm', data=formdata)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')

        links = soup.find_all(attrs={"class": "as-pager-item"})
        titles = soup.find_all(attrs={"class": "as-p-tit"})

        # try:
        #     last_title = LastProject.objects.get(sourceId=2).name
        # except:
        #     last_title = '-1'
        # repeated = False

        for i in range(0,len(titles)):
            data = []
            tmp = titles[i].find_all('span')
            title = tmp[1].text
            date = tmp[2].string[5:]
            link = links[i].get('href')

            # if title == last_title:
            #     repeated = True
            #     break

            data.append(title)
            data.append(date)
            data.append(link)
            data.append(2)
            datas.append(data)
        # if repeated == True:
        #     break

    return datas




def update3():
    titles = Project.objects.get(sourceId=3)
    for title in titles:#titles 取自数据库
        title = title[:-8]
        title = encode_kw(title)
        url = "https://bidnews.cn/caigou/kw-%s" % title + "-zhaobiaogongshi.html"
        res = urllib.request.urlopen(url)
        soup = BeautifulSoup(res)
        tr = soup.find_all('tr')
        td = tr[1].find_all('td')
        title2 = td[2].text
        title = title[:math.floor(0.8 * len(title))]
        title2 = title2[:math.floor(0.8 * len(title2))]
        if title == title2:
            #删除项目信息
            title.delete()
            print("已中标，删除")



def spider3(page_n,kw):
    #https://bidnews.cn/caigou/search.php?kw=%E7%94%B5%E4%BF%A1
    kw = encode_kw(kw)
    datas = []
    for i in range(1,page_n+1):
        # print("page %i" % i + " spiding")
        if i == 1:
            url = "https://bidnews.cn/caigou/search.php?areaid=0&fields=&kw=%s" % kw
        else:
            url = "https://bidnews.cn/caigou/search.php?areaid=0&fields=&kw=%s" % kw + '&page=%i' % i
        res = urllib.request.urlopen(url)
        soup = BeautifulSoup(res)
        tr = soup.find_all('tr')
        # try:
        #     last_title = LastProject.objects.get(sourceId=3).name
        # except:
        #     last_title = '-1'
        # repeated = False
        for i in range(1,34):
            try:
                data = []
                td = tr[i].find_all('td')
                title = td[2].text
                date = td[4].text
                link = td[2].a.get('href')
            except:
                continue
            #
            # if title == last_title:
            #     repeated = True
            #     break

            data.append(title)
            data.append(date)
            data.append(link)
            data.append(3)
            datas.append(data)
        # if repeated == True:
        #     break

    return datas



def update4():
    titles = Project.objects.get(sourceId=4)
    for title in titles:#titles 取自数据库
        title = encode_kw(title)
        url = "https://www.dlzb.com/zhongbiao/search.php?catid=319&areaid=0&kw=%s" % title +"&fields=3"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        soup = BeautifulSoup(res)
        a = soup.find_all(attrs={"class": "gccon_title"})
        if len(a) != 0:
            #删除项目信息
            title.delete()
            print("已中标，删除")



def spider4(page_n,kw):
    kw = encode_kw(kw)
    #https://www.dlzb.com/zb/search.php?kw=%E7%94%B5%E4%BF%A1
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    datas = []
    for i in range(1,page_n+1):
        # print("page %i" % i + " spiding")
        if i == 1:
            url = "https://www.dlzb.com/zb/search.php?kw=%s" % kw
        else:
            url = "https://www.dlzb.com/zb/search.php?kw=%s" % kw + '&page=%i' % i
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        soup = BeautifulSoup(res)
        a = soup.find_all(attrs={"class": "gccon_title"})
        b = soup.find_all(attrs={"class": "gc_date"})
        # try:
        #     last_title = LastProject.objects.get(sourceId=4).name
        # except:
        #     last_title = '-1'
        # repeated = False
        for i in range(0,len(a)):
            data = []
            title = (a[0].text)
            date = (b[0].text)
            link = (a[0].get('href'))

            # if title == last_title:
            #     repeated = True
            #     break

            data.append(title)
            data.append(date)
            data.append(link)
            data.append(4)
            datas.append(data)
        # if repeated == True:
        #     break

    return datas


#二维数组，data[i][0]为标题,[i][1]为日期,[i][2]为网页链接
# data = spider1(NUMBER_PAGE,KEY_WORD) # 一页20条
# data = spider2(NUMBER_PAGE,KEY_WORD) # 一页10条
# data = spider3(NUMBER_PAGE,KEY_WORD) # 一页33条
# data = spider4(NUMBER_PAGE,KEY_WORD) # 一页23条
# print(data[0][1])


# update1()
# update2()
# update3()
# update4()
