# coding=utf-8
import re
import urllib.request
import ssl

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table, DateTime, FLOAT, Text,Time
import urllib

from bs4 import BeautifulSoup

# from ..config import DB_URL
#
# database = 'iot_db'
# engine = create_engine(DB_URL.format(database))
# Base = declarative_base()

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
    for tr in tab.findAll('tr'):
        data = tr.find_all('td')
        if len(data) >4:
            val1 = data[0].find('a').text
            num1 = data[1].text.split()[0]
            num2 = data[2].text.split()[0]
            num3 = data[3].text.split()[0]
            num4 = data[4].text.split()[0]
            print(val1,num1,num2,num3,num4)


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    URL =  "http://www.dongbao120.com/jinrizhujia/"
    soup = getHtml(URL)
    tables=getTables(soup)

    parseTableHeader(tables[1])
    parseTableContent(tables[1])

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.commit()




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