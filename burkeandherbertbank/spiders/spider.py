import scrapy

from scrapy.loader import ItemLoader

from ..items import BurkeandherbertbankItem
from itemloaders.processors import TakeFirst


class BurkeandherbertbankSpider(scrapy.Spider):
	name = 'burkeandherbertbank'
	start_urls = ['https://www.burkeandherbertbank.com/newsroom/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//h6/text()').get()

		item = ItemLoader(item=BurkeandherbertbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
