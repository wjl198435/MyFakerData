# coding=utf-8
import re
import urllib.request
import ssl
import urllib
from datetime import datetime
from bs4 import BeautifulSoup

import sys
sys.path.append("../..")

from config import PIG_PRICE_URL
from dbManager import DBManager, PigPrice

def getHtml(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page)
    page.close()
    return soup

def getTables(content):
    tables = content.findAll('table')
    return tables

def parseTableHeader(table):

    tab = table
    th = tab.find('tr')
    header = th.find_all('th')
    # print("header:",header)
    if len(header) >2:
        h0 = header[0].text.split()[0]
        h1 = header[1].text.split()[0]
        h2 = header[2].text.split()[0]
        h3 = header[3].text.split()[0]
        h4 = header[4].text.split()[0]
        print(h0,h1,h2,h3,h4)

def parseTableContent(table):
    tab = table
    # province,waisanyuan_price,neisanyuan_price,tuzhazhu_price,date=0
    province = []
    waisanyuan_price = []
    neisanyuan_price = []
    tuzhazhu_price = []
    date = []
    for tr in tab.findAll('tr'):
        data = tr.find_all('td')
        if len(data) >4:
            province.append(data[0].find('a').text)
            waisanyuan_price.append(data[1].text.split()[0])
            neisanyuan_price.append(data[2].text.split()[0])
            tuzhazhu_price.append(data[3].text.split()[0])
            date.append(data[4].text.split()[0])
    # print(province,waisanyuan_price,neisanyuan_price,tuzhazhu_price,date)
    return  province,waisanyuan_price,neisanyuan_price,tuzhazhu_price,date

def writeToDB(datas):
    province,waisanyuan_price,neisanyuan_price,tuzhazhu_price,date = datas
    pigPrice=[]
    # print(province)
    # print(waisanyuan_price)
    for i in range(0, len(province)):
        print(i, province[i])
        pp = PigPrice(
            省份 = province[i],
            外三元 = waisanyuan_price[i],
            内三元 = neisanyuan_price[i],
            土杂猪 = tuzhazhu_price[i],
            日期 = datetime.strptime(date[i], '%Y-%m-%d')
        )
        print(datetime.strptime(date[i], '%Y-%m-%d'))
        pigPrice.append(pp)
    dbm =  DBManager()
    dbm.InsertAll(pigPrice)
        # print(i, province[i]）
    # PigPrice(
    # 省份 = 11,
    # 外三元 = 22 ,
    # 内三元 = 112 ,
    # 土杂猪 = 22 ,
    # 日期 = 22,
    # )

def getPigPrice():

    ssl._create_default_https_context = ssl._create_unverified_context
    URL =  PIG_PRICE_URL
    soup = getHtml(URL)
    tables=getTables(soup)

    parseTableHeader(tables[1])
    datas = parseTableContent(tables[1])
    writeToDB(datas)

if __name__ == '__main__':
    getPigPrice()
    # ssl._create_default_https_context = ssl._create_unverified_context
    # URL =  "http://www.dongbao120.com/jinrizhujia/"
    # soup = getHtml(URL)
    # tables=getTables(soup)
    #
    # parseTableHeader(tables[1])
    # datas = parseTableContent(tables[1])
    # writeToDB(datas)






# print("th",th)
# for tr in tab.findFirst('tr'):
#     data = tr.find_all('th')
#     print(data)
# for tr in tab.findAll('tr'):
#     data = tr.find_all('td')
#     if len(data) >2:
#         val1 = data[0].find('a').text
#         num1 = data[1].text.split()[0]
#         num2 = data[2].text.split()[0]
#         num3 = data[3].text.split()[0]
#         num4 = data[4].text.split()[0]
#         print(val1,num1,num2,num3,num4)
# for td in tr.findAll('td'):


# print(td.getText())



# from bs4 import BeautifulSoup
#
# html = """<tbody>
#   <tr>
#     <td><a href="/block_explorer/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa">1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa</a></td>
#     <td><a href="/block_explorer/address/hash/62e907b15cbf27d5425399ebf6f0fb50ebb88f18/">62e907b15cbf27d5425399ebf6f0fb50ebb88f18</a></td>
#     <td class="num">66.6771<small class="b-blockExplorer__small">1246</small>&nbsp;BTC</td>
#     <td class="num">66.6771<small class="b-blockExplorer__small">1246</small>&nbsp;BTC</td>
#     <td class="num">1089</td>
#   </tr>
#   <tr>
#     <td><a href="/block_explorer/address/12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX">12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX</a></td>
#     <td><a href="/block_explorer/address/hash/119b098e2e980a229e139a9ed01a469e518e6f26/">119b098e2e980a229e139a9ed01a469e518e6f26</a></td>
#     <td class="num">50.0572<small class="b-blockExplorer__small">3154</small>&nbsp;BTC</td>
#     <td class="num">50.0572<small class="b-blockExplorer__small">3154</small>&nbsp;BTC</td>
#     <td class="num">55</td>
#   </tr>
#   <!--- SNIP --->
# </tbody>"""
#
# b = BeautifulSoup(html, 'lxml')
# for tr in b.find_all('tr'):
#     data = tr.find_all('td')
#     val1 = data[0].find('a').text
#     val2 = data[1].find('a').text
#     num1 = data[2].text.split()[0]
#     num2 = data[3].text.split()[0]
#     print(val1, val2, num1, num2)