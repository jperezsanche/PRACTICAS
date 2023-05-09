
import scrapy

class testSpider(scrapy.Spider):
    # Nom du scrap. pour l'executer "scrapy crawl annuaire-des-adherents -o test.csv"
    name = "annuaire-des-adherents"
    allowed_domains = ["www.cosmed.fr"]
    
    # Page principale pour scrap
    start_urls ={
        'https://www.cosmed.fr/annuaire-des-adherents/',
    }   
        
    # Ouvrir chaque entreprise dans une page, puis passe à la page suivante
    def parse(self, response):
        # Obtenir liste de sites
        list = response.css('div.posttype-teaser')
        for element in list:
            # Obtenier le lien de chque site et y acceder
            website = element.css('a').xpath('@href').extract()
            yield scrapy.Request(url=website[0], callback=self.parse_site, meta={'website':website})

        # Passer à la page suivante. Click on button next
        next_url = response.css('a.next').xpath('@href').extract_first()
        yield scrapy.Request(url=next_url, callback=self.parse)

    # Fonction pour obtenir les info de l'entreprise dans le site
    def parse_site(self, response):
        
        # Biblioteque avec les info a scrap. A mettre a jours avec info.update(...)
        info = {
                'entreprise':None,
                'website':response.meta['website'],
                'address':None,
                'Activité':None,
                'Téléphone ':None,
                'Email':None,
                'Site':None,
                'SIRET':None,
                'Effectif':None,
                'Activité détaillée':None,
                'Marques distribuées':None,
                'Contacts de la société':None,
                'presentation':None
        }

        # Nom de l'entreprise
        name = response.css('div.info-ste').css('h1::text').extract_first()
        info.update({'entreprise':name})

        # Obtenir l'adresse
        address = ''
        address_list = response.css('div.custom-content-infos').css('div.info').css('p')[0].css('p::text').extract()
        for i in range(len(address_list)):
            address = address + address_list[i].replace(' ', '').replace('\n', ' ').replace(',', ' ')
        info.update({'address':address})
        
        # List des info a gauche du site (Activité, Email, Telefone, Site, SIRET)
        for i in range(1, len(response.css('div.custom-content-infos').css('div.info').css('p')) - 1):
            name_info = response.css('div.custom-content-infos').css('div.info').css('p')[i].css('span::text').extract_first().replace(' ', '').replace('\n', ' ')
            if name_info == "Email":
                data_info = response.css('div.custom-content-infos').css('div.info').css('p')[i].css('p').css('a::text').extract_first()
            else:
                data_info = response.css('div.custom-content-infos').css('div.info').css('p')[i].css('p::text').extract_first()
            data_info = data_info.replace(' ', '').replace('\n', ' ').replace(',', ' ')
            info.update({name_info:data_info})

        # Obtenir les info a droit du site (Activité detailler, Marques distribuées, contacts de la société)
        info_list = response.css('div.col-12').css('div.custom-content-infos')[1].css('div.info')
        for element in info_list:
            info_name = element.css('h3::text').extract_first()
            info_data_list = element.css('ul').css('li::text').extract()
            if len(info_data_list) == 0:
                info_data_list = element.css('p::text').extract() # Marques distribuées est differente
            
            info_data = ""
            for info_element in info_data_list:
                info_element = info_element.replace('\n', '').replace(',', ' ').replace('  ', '').strip()  
                info_data = info_data + "\n" + info_element
            
            info.update({info_name:info_data})

        # Obtenir la presentation de l'entreprise
        presentation = response.css('div.row').css('div.container::text').extract_first()
        if presentation != None:
            presentation = presentation.replace(',', '').replace('\n', ' ')    
        info.update({'presentation':presentation})

        # Ecrir l'information recuperé dans le fichier
        yield info