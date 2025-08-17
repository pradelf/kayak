import scrapy
import logging


lieux= ["Mont Saint Michel",
"St Malo",
"Bayeux",
"Le Havre",
"Rouen",
"Paris",
"Amiens",
"Lille",
"Strasbourg",
"Chateau du Haut Koenigsbourg",
"Colmar",
"Eguisheim",
"Besancon",
"Dijon",
"Annecy",
"Grenoble",
"Lyon",
"Gorges du Verdon",
"Bormes les Mimosas",
"Cassis",
"Marseille",
"Aix en Provence",
"Avignon",
"Uzes",
"Nimes",
"Aigues Mortes",
"Saintes Maries de la mer",
"Collioure",
"Carcassonne",
"Ariege",
"Toulouse",
"Montauban",
"Biarritz",
"Bayonne",
"La Rochelle"]

mapping={}
def liste_villes()->list:
    liste_retour=[]
    for lieu in lieux:
        url=f"https://www.booking.com/searchresults.fr.html?ss={lieu.replace(' ','+')}"
        mapping[url]=lieu
        liste_retour.append(url)
    return liste_retour
    

class BookingSpider(scrapy.Spider):
    name = "booking"
    allowed_domains = ["booking.com"]
    start_urls = liste_villes()
    def parse_coordinates(self,response):
        hotel = response.meta['hotel']
        hotel['coordinates'] = response.xpath('//a[1]/@data-atlas-latlng').get()
        yield hotel

    def parse(self, response):
        #ville=response.xpath('/html/body/div[4]/div/div/div/div[1]/div/form/input[1]/@value').get()
        ville=mapping[response.request.url]
        hotels = response.xpath('//div[contains(@data-testid,"property-card")]')
        
        logging.info('No next page. Terminating crawling process.')
        for hotel in hotels:
            if (hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get()!=None):
                #logging.info(room.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div[1]/div//div/@aria-label').get())#/@aria-label
                stars=hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div[1]/div//div/@aria-label').get()
                url=hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/@href').get()
                nom=hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get()
                description=hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[3]/text()').get(),
                hotel={
                    'ville' : ville,
                    'nom': nom,
                    'url': url,
                    'description': description,
                    'stars': stars,
                }
                yield response.follow(url=url,callback=self.parse_coordinates, meta={'hotel':hotel})
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

# /html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[3]
# /html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]
# /html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a
# /html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]
# /html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]
#ville : /html/body/div[4]/div/div/div/div[1]/div/form/input[1]/@value
# xpath sure la page d'un hotel
# nom hotel : //div[@id="hp_hotel_name"]/div/h2
# url : celle de l'appel
# nombre étoile : //button[@data-testid="quality-rating"]/@aria-label
# description : //p[@data-testid="property-description"]/text()
# coordinates : //a[1]/@data-atlas-latlng
