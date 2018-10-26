# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException


class RunSpider(Spider):
    name = 'run'
    allowed_domains = ['amazon.co.uk']
    start_urls = ['https://www.amazon.co.uk/s?marketplaceID=A1F83G8C2ARO7P&me=AGX3G9AHLXSYJ&merchant=AGX3G9AHLXSYJ']

    def parse(self, response):
        items = response.xpath('//div[@class="a-section a-spacing-none a-inline-block s-position-relative"]/a/@href').extract()
        for item in items:
            yield Request(item, callback=self.parse_item)
        # process next page
        next_page_url = response.xpath('//a[@title="Next Page"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_item(self, response):
        title = response.xpath('//span[@id="productTitle"]/text()').extract_first().strip()

        customer_price = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first().strip()

        product_url = response.url
        self.driver = webdriver.Chrome()
        self.driver.get(product_url)

        sel = Selector(text=self.driver.page_source)

        Price = sel.xpath('//div[@class="a-text-center a-spacing-mini"]/span[@class="a-color-price"]/text()').extract_first()
        Price = sel.xpath('//*[@id="unqualifiedBuyBox"]/div/div[1]/span/text()').extract_first()

        # amazon_price_page = self.driver.find_element_by_xpath('//span[@class="olp-padding-right"]/a/@href')
        # sleep(3)
        # self.logger.info('Sleeping for 3 seconds.')
        # amazon_price_page.click()

        # sel = Selector(text=self.driver.page_source)
        # amazon_price = sel.xpath('//h3/a/@href').extract() 
        # response.xpath('//div[@class="a-row a-spacing-mini olpOffer"]').extract()      


        yield {
            'Title': title,
            'Customer Price': customer_price,
            'Price': Price,
            'product_url': product_url,
        }
