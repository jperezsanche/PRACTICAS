import os

scraps_list = ['annuaire-des-adherents']

for scrap in scraps_list:
    os.system("scrapy crawl " + scrap + " -o " + scrap + ".csv")