# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:10:23 2021

@author: 22gulsethj
"""
import logging
import warnings
from typing import Optional


from scrapy import signals
from scrapy.http import Request
from scrapy.utils.trackref import object_ref
from scrapy.utils.url import url_is_from_spider
from scrapy.utils.deprecate import method_is_overridden
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.spiders.feed import XMLFeedSpider, CSVFeedSpider
from scrapy.spiders.sitemap import SitemapSpider

class Spider(object_ref):
     name: Optional[str] = None
     custom_settings: Optional[dict] = None

def __init__(self, name=None, **kwargs):
    if name is not None:
        self.name = name
    elif not getattr(self, 'name', None):
        raise ValueError(f"{type(self).__name__} must have a name")
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})
    def log(self, message, level=logging.DEBUG, **kw):
        """Log the given message at the given log level

        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.
        """
        self.logger.log(level, message, **kw)
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider


    def _set_crawler(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        crawler.signals.connect(self.close, signals.spider_closed)

    def start_requests(self):
        cls = self.__class__
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        if method_is_overridden(cls, Spider, 'make_requests_from_url'):
            warnings.warn(
                "Spider.make_requests_from_url method is deprecated; it "
                "won't be called in future Scrapy releases. Please "
                "override Spider.start_requests method instead "
                f"(see {cls.__module__}.{cls.__name__}).",
            )
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        else:
            for url in self.start_urls:
                yield Request(url, dont_filter=True)


    def make_requests_from_url(self, url):
        """ This method is deprecated. """
        warnings.warn(
            "Spider.make_requests_from_url method is deprecated: "
            "it will be removed and not be called by the default "
            "Spider.start_requests method in future Scrapy releases. "
            "Please override Spider.start_requests method instead."
        )
        return Request(url, dont_filter=True)

    def _parse(self, response, **kwargs):
        return self.parse(response, **kwargs)

    def parse(self, response, **kwargs):
        raise NotImplementedError(f'{self.__class__.__name__}.parse callback is not defined')
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(cls.custom_settings or {}, priority='spider')

    @classmethod
    def handles_request(cls, request):
        return url_is_from_spider(request.url, cls)

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)

    def __str__(self):
        return f"<{type(self).__name__} {self.name!r} at 0x{id(self):0x}>"

    __repr__ = __str__


# Top-level imports
