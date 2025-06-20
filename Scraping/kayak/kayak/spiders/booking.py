import scrapy


class BookingSpider(scrapy.Spider):
    name = "booking"
    allowed_domains = ["booking.com"]
    start_urls = [  'https://www.booking.com/searchresults.fr.html?ss=Mont+Saint+Michel+France',
                    'https://www.booking.com/searchresults.fr.html?ss=St+Malo+France',
                    'https://www.booking.com/searchresults.fr.html?ss=Bayeux+France']
    def parse(self, response):
        rooms = response.xpath('/html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[3]')
        for quote in quotes:
            yield {
                'nom': quote.xpath('div[4]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/div[1]/text()').get(),
                'url': quote.xpath('div[4]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/text()').get(),
            }

        try:
            # Select the NEXT button and store it in next_page
            # Here we include the class of the li tag in the XPath
            # to avoid the difficujlty with the "previous" button
            next_page = response.xpath('/html/body/div/div[2]/div[1]/nav/ul/li[@class="next"]/a').attrib["href"]
        except KeyError:
            # In the last page, there won't be any "href" and a KeyError will be raised
            logging.info('No next page. Terminating crawling process.')
        else:
            # If a next page is found, execute the parse method once again
            yield response.follow(next_page, callback=self.parse)

