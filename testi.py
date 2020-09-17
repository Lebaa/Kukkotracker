import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

start = datetime.now()

def find_element(driver, xpath):
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath,))
    )
    return element

def sloop(d,kauppa):
    print("Dasd")
    e = find_element(d,"/html/body/div[5]/div[2]/header/div[3]/div/div[1]/div/nav/ul/li[4]/div/a/span",)
    e.click()
    sleep(5)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(kauppa)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(Keys.ENTER)
    e = find_element(
        d,
        "/html/body/div[5]/div[2]/div[7]/div/div[3]/div[2]/div/ul/li[1]/div[1]/div[1]/a[2]",
    )
    e.click()
    e = find_element(d, "/html/body/div[5]/div[2]/header/div[2]/div/div/div/div/a")
    e.click()
    sleep(5)
    for s in slinkit:
        print(s)
        d.get(s)
        soppa = BeautifulSoup(d.page_source, 'html.parser')

        try:
            hinta1 = soppa.find("span", {"class": "whole-number"}).text
            hinta2 = soppa.find("span", {"class": "decimal"}).text
            hinta = hinta1 + "," + hinta2
            print(hinta)
        except AttributeError:
            print("eio")

def kloop(driver, k):

    e = find_element(
        driver, "/html/body/div[1]/section/header/div[1]/nav/ul[1]/li[1]/a/span"
    )
    e.click()
    e = find_element(
        driver,
        "/html/body/div[1]/section/header/div[1]/nav/ul[2]/div/nav/div[2]/div/span/span",
    )
    e.click()
    e = find_element(driver, "/html/body/div[2]/div[1]/div/div[3]/form/div/div/input")
    e.send_keys(k)
    sleep(3)
    e = find_element(
        driver, "/html/body/div[2]/div[1]/div/div[3]/div/div/a[1]/div[1]"
    )
    e.click()
    for l in linkit:
        driver.get(l)
        sleep(2)
        soppa = BeautifulSoup(driver.page_source, 'html.parser')
        hinta = soppa.find("span", {"class": "price"}).text
        if "€" in hinta or "/kpl" in hinta:
            print("eio")
        else:
            print(hinta)

linkit = ["https://www.k-ruoka.fi/kauppa/tuote/sandels-47-033l-tlk-8-pack-6419800020271",
"https://www.k-ruoka.fi/kauppa/tuote/sandels-47-033l-tlk-18-p-dolly-6419802021238",
"https://www.k-ruoka.fi/kauppa/tuote/sandels-47-033l-24-pac-tlk-dolly-6419802020491",
"https://www.k-ruoka.fi/kauppa/tuote/kukko-lager-47-033l-tlk-12-pack-dolly-6418654202024",
"https://www.k-ruoka.fi/kauppa/tuote/kukko-lager-olut-47-033l-tlk-6-pack-6418654204387",
"https://www.k-ruoka.fi/kauppa/tuote/a-le-coq-premium-45-033l-tlk-8-pack-6419800021285",
"https://www.k-ruoka.fi/kauppa/tuote/a-le-coq-45-033l-tlk-18-pack-dolly-6419800022268",
"https://www.k-ruoka.fi/kauppa/tuote/a-le-coq-prem-45-033l-tlk-24-pack-dol-6419802022136",
"https://www.k-ruoka.fi/kauppa/tuote/karhu-olut-46-033l-tlk-8-pack-6415600002806",
"https://www.k-ruoka.fi/kauppa/tuote/karhu-iii-033l-18-pack-46-tlk-dolly-6415600512961",
"https://www.k-ruoka.fi/kauppa/tuote/karhu-olut-46-033l-tlk-24-pack-dolly-6415600020152",
"https://www.k-ruoka.fi/kauppa/tuote/pirkka-iii-olut-033l-45-tlk-24-p-6410405091284",
"https://www.k-ruoka.fi/kauppa/tuote/pirkka-iii-olut-033l-46-tlk-12-pack-6410405113306",
"https://www.k-ruoka.fi/kauppa/tuote/karjala-olut-45-033l-tlk-6-pack-6413605094161",
"https://www.k-ruoka.fi/kauppa/tuote/karjala-olut-45-033l-tlk-8-pack-6413605142152",
"https://www.k-ruoka.fi/kauppa/tuote/karjala-olut-45-033l-tlk-24-pack-doll-6413601094219",
"https://www.k-ruoka.fi/kauppa/tuote/olvi-iii-45-033l-tlk-8-pack-6419800020417",
"https://www.k-ruoka.fi/kauppa/tuote/olvi-iii-45-033l-tlk-24-pack-dolly-6419802020217"]

slinkit = ["https://www.foodie.fi/entry/6419800020271",
"https://www.foodie.fi/entry/6419802021238",
"https://www.foodie.fi/entry/6419802020491",
"https://www.foodie.fi/entry/6418654202024",
"https://www.foodie.fi/entry/6418654204387",
"https://www.foodie.fi/entry/6419800021285",
"https://www.foodie.fi/entry/6419800022268",
"https://www.foodie.fi/entry/6419802022136",
"https://www.foodie.fi/entry/6415600002806",
"https://www.foodie.fi/entry/6415600512961",
"https://www.foodie.fi/entry/6415600020152",
"https://www.foodie.fi/entry/6410405091284",
"https://www.foodie.fi/entry/6410405113306",
"https://www.foodie.fi/entry/6413605094161",
"https://www.foodie.fi/entry/6413605142152",
"https://www.foodie.fi/entry/6413601094219",
"https://www.foodie.fi/entry/6419800020417",
"https://www.foodie.fi/entry/6419802020217"]



skaupat = [
    "Mestarin Herkku",
    "Prisma Keljo Jyväskylä",
    "Prisma Palokka",
    "Prisma Seppälä Jyväskylä",
    "S-market Kolmikulma",
    "S-market Kuokkala",
    "S-Market Palokka",
    "S-market Savela",
]

kaupat = [
    "K-Citymarket Jyväskylä Palokka",
    "K-Citymarket Keljo",
    "K-Citymarket Seppälä",
    "K-Supermarket Kotikenttä",
    "K-Supermarket Lutakko",
    "K-Supermarket Länsiväylä",
    "K-Market Ainola",
    "K-Market Aittorinne",
    "K-Market Kotiväylä",
    "K-Market Kuokkalanpelto",
    "K-Market Schaumanin puistotie",
    "K-Market Torikeskus",
]

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
driver.get("https://www.k-ruoka.fi/")

for k in kaupat:
    kloop(driver, k)

d = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
d.get("https://www.foodie.fi")
e = find_element(d, "/html/body/div[8]/div/div[2]/div/button[1]")
e.click()
sleep(2)

for skau in skaupat:
    sloop(d, skau)
d.close()

driver.close()
print("Skriptin kesto: " + str(datetime.now() - start))


