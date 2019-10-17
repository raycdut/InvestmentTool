# -*- coding: utf-8 -*-
import scrapy
import json
import demjson
from fund_scrapy.items import Fund


class FundListSpider(scrapy.Spider):
    name = 'fund_list'
    allowed_domains = ['http://fund.eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page=1,200&dt=1571234671718&atfc=&onlySale=0']

    def __init__(self):
        self.start_index = 1  # start page index
        self.max_index = 40  # max page index

    def parse(self, response):
        print('current page : {0}'.format(response.url))
        strResult = response.text[7:]
        resultobj = demjson.decode(strResult)

        # return fund data start
        for item in resultobj['datas']:
            fund = Fund()
            fund['FundCode'] = item[0]
            fund['FundDescription'] = item[1]
            fund['FundBuyStatus'] = item[9]
            fund['FundSellStatus'] = item[10]
            if item[-3]:
                fund['FundFee'] = float(item[-3].strip('%')) / 100
            else:
                fund['FundFee'] = 0.00

            yield fund
        # return fund data end

        # process next page if have.

        self.max_index = int(resultobj['pages'])
        nextUrl = self.get_next_page(response.status)
        if self.start_index <= self.max_index:
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    def get_next_page(self, status):
        if status == 200:
            self.start_index = self.start_index+1

        nextpage = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page={0},200&dt=1571234671718&atfc=&onlySale=0'.format(
            self.start_index)
        return nextpage
