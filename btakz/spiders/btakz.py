import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from btakz.items import Article


class btakzSpider(scrapy.Spider):
    name = 'btakz'
    start_urls = ['https://bta.kz/en/press/news/']

    # def parse(self, response):


    def parse(self, response):
        links = response.xpath('//a[@class="clspd_subject"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url.lower():
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="smldt"]/text()').get()
        if date:
            date = " ".join(date.split())

        content = response.xpath('//div[@class="content"]//p//text()').getall()
        content = [text.strip() for text in content if text.strip() and '{' not in text]
        content = " ".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
