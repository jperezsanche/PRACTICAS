import scrapy

class testSpider(scrapy.Spider):
    name = "cosmetiques_sous-traitant" # Nom du scrap
    allowed_domains = ["www.europages.fr"]
    start_urls ={
        'https://www.europages.fr/entreprises/sous-traitant/cosmetique.html', # liste de URL à analiser
    }   
        
    # Fonction de scrap
    def parse(self, response):
        card_list = response.css('li.ep-ecard') # Recherche des conteneurs css
        for card in card_list:
            entreprise = card.css('p.text-subtitle-1::text').extract()
            website = card.css('a.ep-simple-link').xpath('@href').extract()
            description_old = card.css('p.ep-ecard__description::text').extract()
            description = []
            for desc in description_old:
                desc = desc.replace('\n', '  ').replace('\r', ' ').replace(',', ' ')
                description.append(desc)

            # Données recuperes à sauvgarder
            yield {
                'entreprise':entreprise,
                'description':description,
                'website':website
                }
        
        # Obtenir le lien de la page suivante
        next_url_list = response.css('a.ep-server-side-pagination__prev-next').xpath('@href').extract()
        next_url = next_url_list[len(next_url_list) - 1]
        next_url = 'https://www.europages.fr'+next_url
        yield scrapy.Request(url=next_url, callback=self.parse)