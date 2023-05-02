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

## Function to transform list of dict to string with ";" sperator
def transformListOfDict(dct):
    return ";".join(str(value) for value in dct.values())


#Recherche sur LinkedIn de groupes de personnes avec le terme spécifié et collecte de noms et d-URLS correspondants.
#terme_recherche : cosmetic
#Retour : liste de groupes de distributeurs, liste d-autres groupes de cosmetic 
#Par exemple : recherche_candidat, Distributors



##Parameters that can be modified

#Utilisation d-email et mdp provisoir pour collecter les données:
#email: alondra.stage@gmail.com
#mdp: stage2023
#Posibilité de changer le mot cle de (recherche) selon les groupes qui souhaitent trouver

startPage=1
nbPageToScrap=100
filename="recherche_prospects.csv"
email = "alondra.stage@gmail.com"
password = "stage2023"
recherche = ("Essais+cliniques", "Tolérance+et+efficacité", "Test+de+patch" , "Test+en+cours+d'utilisation"
"Évaluation+instrumentale+et+perçue", "Dermatologie", "Gynécologie", "Ophtalmologie", "Esthétique", "Cosmétique", "Dispositifs+médicaux",
"Dosages+in+vitro", "Ingrédients", "Peau", "Oculaire", "Irritation", "Sensibilisation", "Phototoxicité", "Passage+transcutané", "Hépatotoxicologie", "Interactions+médicamenteuses", 
"Lecture+génomique", "LC-MS/MS", "Dosages+enzymatiques","Imagerie","Isotopes+radioactifs", "Toxicologie+réglementaire")



##Driver initialization
chrome_options = Options()
#chrome_options.binary_location = "C:/webdriver/chrome106/chrome.exe"
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


##Linkedin connexion
actions.login(driver, email, password)

time.sleep(1)

compteur = 0

# Create a file (erase if exist) : 
file = open(filename, "w")
file_distributors = open("Distributors.csv", "w")
file_academy = open("Academy.csv", "w")
file_producteurs = open("producteurs.csv", "w")

prospects=[]
file.write("name;url;description" + "\n")
file_distributors.write("name;url;description" + "\n")
file_academy.write("name;url;description" + "\n")
file_producteurs.write("name;url;description" + "\n")

##Scrapping
def scrappLinkedIn(term,type_prospect):
    for page in range(startPage,nbPageToScrap+1):
        driver.get("https://www.linkedin.com/search/results/groups/?keywords=" + recherche + "&origin=GLOBAL_SEARCH_HEADER&page=" + str(page) + "&sid=kts")

        webElems=[]
        webElems=driver.find_elements(By.XPATH,"//a[contains(@href,'https://www.linkedin.com/groups/')]")

        urlProfiles=[]
        for aBalise in webElems :
            if aBalise.get_attribute("href") not in urlProfiles:
                urlProfiles.append(aBalise.get_attribute("href"))

        time.sleep(1)

        for url in urlProfiles:
            driver.get(url)
            try:
                compteur = compteur + 1
                # Obtenir le nom du group
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

                if (desc.find("distributor") != -1 or desc.find("distributeur") != -1) :
                    csvline = transformListOfDict({'name': name, 'jobTitle': None,'url': url, 'description': desc})
                    file_distributors.write(csvline + "\n")
                    file_distributors.flush()


                if (desc.find("producteur") != -1 or desc.find("producer") != -1) :
                    csvline = transformListOfDict({'name': name,'url': url, 'description': desc})
                    file_producteurs.write(csvline + "\n")
                    file_producteurs.flush()

                if (desc.find("academie") != -1 or desc.find("academy") != -1) :
                    csvline = transformListOfDict({'name': name,'url': url, 'description': desc})
                    file_academy.write(csvline + "\n")
                    file_academy.flush()



                prospects.append({'name': name,'url': url, 'description' : desc})
                csvline = transformListOfDict({'name': name,'url': url,'description': desc})
                file.write(csvline + "\n")
                file.flush()
            except Exception as e:
                time.sleep(1)
                continue

            time.sleep(1)
            
    
    if __name__ == "__main__":
    import sys
    search_term = sys.argv[1]
    prospect_typology = sys.argv[2]
    # run main function
    scrappLinkedIn(search_term,prospect_typology)


driver.quit()
