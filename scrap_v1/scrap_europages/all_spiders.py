import os

scraps_list = ['cosmetiques', 'cosmetiques_distribuitor', 'cosmetiques_sous-traitant', 'cosmetiques_agent', 'cosmetiques_detaillant', 'cosmetiques_prestataire','cosmetiques_grossiste','cosmetiques_producteur']

for scrap in scraps_list:
    os.system("scrapy crawl " + scrap + " -o " + scrap + ".csv")