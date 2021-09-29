# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 12:57:44 2021

@author: 22gulsethj
"""
import scrapy 
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class scraper(scrapy.Spider):
    name = 'military.wikia.org'
    allowed_domains = ['military.wikia.org']
    start_urls = ['https://military.wikia.org/']

    def parse(self, response):
        pass
 