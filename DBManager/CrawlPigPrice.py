# coding=utf-8
import re
import urllib.request
import ssl
import urllib
from datetime import datetime
from bs4 import BeautifulSoup

import sys
sys.path.append("..")

from utils.logger import info, setInfo,error,debug
# import sys
# sys.path.append("../..")

from config import PIG_PRICE_URL
from DBManager.createBigDataTables import PigPriceTable,getBigDataBaseSession
from DBManager.createIOTables import getIotDataBaseSession
from DBManager.dbManager import DBManager


class PigPrice(object):

    def __init__(self,url):
        """Initialize processor thread"""
        debug('ProcessorThread init')
        self._url = url

    def getPigPrice(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        URL = self._url
        soup = self.getHtml(URL)
        tables = self.getTables(soup)

        self.parseTableHeader(tables[1])
        datas = self.parseTableContent(tables[1])
        print(datas)
        self.writeToDB(datas)

    def writeToDB(self,datas):
        province,waisanyuan_price,neisanyuan_price,tuzhazhu_price,date = datas
        pigPrice=[]
        # print(province)
        # print(waisanyuan_price)
        for i in range(0, len(province)):
            print(i, province[i])
            pp = PigPriceTable(
                省份 = province[i],
                外三元 = waisanyuan_price[i],
                内三元 = neisanyuan_price[i],
                土杂猪 = tuzhazhu_price[i],
                日期 = datetime.strptime(date[i], '%Y-%m-%d')
            )
            print(datetime.strptime(date[i], '%Y-%m-%d'))
            pigPrice.append(pp)
        dbm =  DBManager(getBigDataBaseSession())
        dbm.InsertAll(pigPrice)

    def getHtml(self,url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page)
        page.close()
        return soup

    def getTables(self,content):
        tables = content.findAll('table')
        return tables

    def parseTableHeader(self,table):

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

    def parseTableContent(self,table):
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

def get_pig_price():
    debug("debug")
    pp=PigPrice(PIG_PRICE_URL)
    pp.getPigPrice()

if __name__ == '__main__':
    pp=PigPrice(PIG_PRICE_URL)
    pp.getPigPrice()
    # getPigPrice()
