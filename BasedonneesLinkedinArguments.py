#Ce script extrait les noms et URL de groupes trouvés avec le mot clé « cosmetic » sur LinkedIn.
#Auteur : j.perez@wepredic.com
#Date : 24/04/2023
#Use : BasedeDonneesLinkedin.py 


##Librairies import
from selenium import webdriver
from selenium.webdriver.common.by import By
from linkedin_scraper import Person,actions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import os

## Function to transform list of dict to string with ";" sperator
def transformListOfDict(dct):
    return ";".join(str(value) for value in dct.values())

##Parameters that can be modified

#Utilisation d-email et mdp provisoir pour collecter les données:
#email: alondra.stage@gmail.com
#mdp: stage2023
#Posibilité de changer le mot cle de (recherche) selon les groupes qui souhaitent trouver

startPage=1
nbPageToScrap=1
filename="recherche_prospects.csv"
email = "alondra.stage@gmail.com"
password = "stage2023"

## Fonction princiapl de scarp
def main(recherche, type_prospect):
    compteur = 0

    os.mkdir(recherche)

    # Create a file (erase if exist) : 
    filename = recherche + "_prospects.csv"
    file = open(recherche + "/" + filename, "w")
    file.write("name;url;description" + "\n")

    # Creer un ficher par type de prospecte
    file_per_type = [None] * len(type_prospect) # List de file object
    for i in range(0,len(type_prospect)):
        file_type_name=recherche + "_" + type_prospect[i] + "_type.csv"
        file_per_type[i] = open(recherche + "/" + file_type_name, "w")
        file_per_type[i].write("name;url;description" + "\n")
        file_per_type[i].flush()
    
    # Farie la recher d'une page linkedin (10 groupes par page normalement)
    for page in range(startPage,nbPageToScrap+1):
        driver.get("https://www.linkedin.com/search/results/groups/?keywords=" + recherche + "&origin=GLOBAL_SEARCH_HEADER&page=" + str(page) + "&sid=kts")

        webElems=[]
        webElems=driver.find_elements(By.XPATH,"//a[contains(@href,'https://www.linkedin.com/groups/')]")

        urlProfiles=[]
        for aBalise in webElems :
            if aBalise.get_attribute("href") not in urlProfiles:
                urlProfiles.append(aBalise.get_attribute("href"))

        time.sleep(1)

        # Liste des groupes par page (10 par page)
        for url in urlProfiles:
            driver.get(url)
            try:
                compteur = compteur + 1
                WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, "//h1/span"))
                )
                nameElems=driver.find_elements(By.XPATH,"//h1/span")
                name = nameElems[0].text
                print(compteur, end="")
                print(" - Name: " + name)

                # Obtenir la description et separer les distributeurs
                nameElems=driver.find_elements(By.XPATH,"//p/span")
                desc = nameElems[0].text #cette ligne récupere le texte de la description et le collecte dans la variable desc
                desc = desc.replace('\n', '  ').replace('\r', ' ')

                # Chercher chaque type de prospect par mot dans la descirption du gorupe
                # Si mot toruvé, l'ajouter dans le fichier correspondant
                for i in range(len(type_prospect)):
                    if (desc.find(type_prospect[i]) != -1) :
                        csvline = transformListOfDict({'name': name, 'jobTitle': None,'url': url, 'description': desc})
                        file_per_type[i].write(csvline + "\n")
                        file_per_type[i].flush()

                # BDD principale
                csvline = transformListOfDict({'name': name,'url': url,'description': desc})
                file.write(csvline + "\n")
                file.flush()
            except Exception as e:
                time.sleep(1)
                print(e)
                continue

            time.sleep(1)
        file.close()

##
# Debut du programme       
##   

if __name__ == "__main__":
    import sys

if len(sys.argv) < 3:
    print("")
    print("Erreur, vous devez fournir un mot clé encodé pour URL et une liste de type separé par des spaces")
    print("     Syntax: <key%20word> <type1> [tyep2_facultatif] [tyep3_facultatif] ...")
    print("     Example: clinical%20trials producer distributor laboratory animals")
    print("")
    quit() # exit

# mot clé
print("Mot clé: " + sys.argv[1])
search_term = sys.argv[1]

# Types
prospect_typology = []
for i in range(2, len(sys.argv)):
    print("Type de prospect: " + sys.argv[i])
    prospect_typology.append(sys.argv[i])

print(prospect_typology)

##Driver initialization
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

##Linkedin connexion
actions.login(driver, email, password)

time.sleep(1)

# run main function
main(search_term, prospect_typology)


driver.quit()
