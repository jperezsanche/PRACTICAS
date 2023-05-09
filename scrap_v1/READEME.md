# Utilisation Scrapy

## Creer un nouveau projet

commande à exécuter depuis la racine. Un dossier va être généré : ```scrapy startproject <Nom-projet>```

Se deplacer dans la ligne de commande vers le dossier cree (le dossier est nomé peril que le projet). Depuis cette nouveau dossier, on doit exécuter le reste des commandes.

## Creer un nouveau spider

Un spider et le code pous scrap un site spécifique.

Nous allons creer un fichier que nous allons nommer en fonction du scrap à réaliser, par example distribuitors.py. Ce fichier doit conternir, au moins le code suivante.

```python

import scrapy

class testSpider(scrapy.Spider):
    name = "distribuitors" # Nom du scrap
    allowed_domains = ["www.europages.fr"]
    start_urls ={
        'https://www.europages.fr/entreprises/cosmetique.html', # liste de URL à analiser
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
```

Ce code est execute à l'aide la fa commande suivante : `scrapy crawl distribuitors -o test.csv`. Scrapy crawl sont les outils de scrap. distribuitors c'est le nom que l'on a défini dans le code (`name='distribuitors'`), et `-o distribuitors.csv` est le fichiers qui va être généré par

C'est possible de faire un script "wrap" qui lui va appeler plusieurs fois scrapy pour demander plusieurs spiders d'affilé. C'est possible en faisant `python all_spiders.py`