import scrapy
from ..items import KartonageItem

class KartonSpider(scrapy.Spider):
    name = "kartons12"
    allow_domains = ['karton.eu']
    start_urls = [
        'https://www.karton.eu/Faltkartons'
        ]
    custom_settings = {'FEED_EXPORT_FIELDS': ['SKU', 'Title', 'Link', 'Price', 'Delivery_Status', 'Weight', 'QTY', 'Volume'] } 
    
    def parse(self, response):
        url = response.xpath('//div[@class="cat-thumbnails"]')

        for a in url:
            link = a.xpath('a/@href')
            yield response.follow(url=link.get(), callback=self.parse_category_cartons)

    def parse_category_cartons(self, response):
        url2 = response.xpath('//div[@class="cat-thumbnails"]')

        if not url2:
            print('Empty url2:', response.url)

        for a in url2:
            link = a.xpath('a/@href')
            yield response.follow(url=link.get(), callback=self.parse_target_page)

    def parse_target_page(self, response):
        card = response.xpath('//div[@class="text-center artikelbox"]')

        for a in card:
            items = KartonageItem()
            link = a.xpath('a/@href')
            items ['SKU'] = a.xpath('.//div[@class="delivery-status"]/small/text()').get()
            items ['Title'] = a.xpath('.//h5[@class="title"]/a/text()').get()
            items ['Link'] = a.xpath('.//h5[@class="text-center artikelbox"]/a/@href').extract()
            items ['Price'] = a.xpath('.//strong[@class="price-ger price text-nowrap"]/span/text()').get()
            items ['Delivery_Status'] = a.xpath('.//div[@class="signal_image status-2"]/small/text()').get()
            yield response.follow(url=link.get(),callback=self.parse_item, meta={'items':items})

    def parse_item(self,response):
        table = response.xpath('//div[@class="product-info-inner"]')

        #items = KartonageItem() # You don't need this here, as the line bellow you are overwriting the variable.
        items = response.meta['items']
        items['Weight'] = response.xpath('.//span[@class="staffelpreise-small"]/text()').get()
        items['Volume'] = response.xpath('.//td[@class="icon_contenct"][7]/text()').get()
        yield items