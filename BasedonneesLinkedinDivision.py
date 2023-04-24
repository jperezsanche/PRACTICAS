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

##Parameters that can be modified
startPage=1
nbPageToScrap=100
filename="recherche_candidat.csv"
email = "alondra.stage@gmail.com"
password = "stage2023"
recherche = "cosmetic"


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

prospects=[]
file.write("name;jobTitle;experiences;url" + "\n")
file_distributors.write("name;jobTitle;experiences;url" + "\n")
##Scrapping
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
            desc = nameElems[0].text
            if (desc.find("distributor") != -1 or desc.find("distributeur") != -1) :
                csvline = transformListOfDict({'name': name, 'jobTitle': None, 'experiences': None, 'url': url})
                file_distributors.write(csvline + "\n")
                file_distributors.flush()

            prospects.append({'name': name, 'jobTitle': None, 'experiences': None, 'url': url})
            csvline = transformListOfDict({'name': name, 'jobTitle': None, 'experiences': None, 'url': url})
            file.write(csvline + "\n")
            file.flush()
        except Exception as e:
            time.sleep(1)
            continue
            
        time.sleep(1)




driver.quit()