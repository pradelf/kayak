import scrapy


class BookingSpider(scrapy.Spider):
    name = "booking"
    allowed_domains = ["booking.com"]
    start_urls = ["https://www.booking.com/searchresults.fr.html?ss=Paris%2C+France&checkin=2025-05-27&checkout=2025-06-04"]

    def parse(self, response):
        pass
