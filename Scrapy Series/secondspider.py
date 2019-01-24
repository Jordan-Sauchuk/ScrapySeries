#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 13:33:11 2018

@author: jordansauchuk
"""


import scrapy
from example.items import MovieItem

class ThirdSpider(scrapy.Spider):
    name = "imdbtestspider"
    allowed_domains = ["imdb.com"]
    start_urls = (
        'http://www.imdb.com/chart/top',
    )

    def parse(self, response):
        links = response.xpath('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]/a/@href').extract()
        i =1 
        for link in links:
            abs_url = response.urljoin(link)
            url_next = '//*[@id="main"]/div/span/div/div/div[2]/table/tbody/tr['+str(i)+']/td[3]/strong/text()'
            rating = response.xpath(url_next).extract()
            if (i <= len(links)):
                i=i+1
            yield scrapy.Request(abs_url, callback = self.parse_indetail, meta={'rating' : rating})
       


    def parse_indetail(self,response):
        item = MovieItem()
        item['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0][:-1]
        item['directors'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="director"]/a/span/text()').extract()[0]
        item['writers'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="creator"]/a/span/text()').extract()
        item['stars'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="actors"]/a/span/text()').extract()
        item['popularity'] = response.xpath('//div[@class="titleReviewBarSubItem"]/div/span/text()').extract()[2][21:-8]
        
        return item

     












































import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'SDS'
    allowed_domains = ['www.superdatascience.com']
    start_urls = ['http://www.superdatascience.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item