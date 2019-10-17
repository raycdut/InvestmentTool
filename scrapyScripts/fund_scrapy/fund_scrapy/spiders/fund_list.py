# -*- coding: utf-8 -*-
import scrapy
import json
import demjson


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

        self.max_index = int(resultobj['pages'])
        nextUrl = self.get_next_page(response.status)
        if self.start_index < self.max_index:
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    def get_next_page(self, status):
        if status == 200:
            self.start_index = self.start_index+1

        nextpage = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page={0},200&dt=1571234671718&atfc=&onlySale=0'.format(
            self.start_index)
        return nextpage
