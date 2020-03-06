from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import sqlite3
from selenium.common.exceptions import NoSuchElementException

conn = sqlite3.connect("kukko.db")
c = conn.cursor()


#def create_table():
 #   c.execute("CREATE TABLE IF NOT EXISTS tuote (id INTEGER PRIMARY KEY, kauppa_id INTEGER, nimi TEXT, hinta TEXT, date TEXT, FOREIGN KEY(kauppa_id) REFERENCES kaupat(id))")


#def insert_kaupat(kauppa,ketju):
  #  c.execute("INSERT INTO kaupat (nimi, ketju) VALUES (?, ?)", (kauppa,ketju))
   # conn.commit()

def hinta_tauluun(kauppa_id, nimi, hinta, date):
    c.execute(("INSERT INTO tuote (kauppa_id, nimi, hinta, date) VALUES (?,?,?,?"), (kauppa_id,nimi,hinta,date))
    conn.commit()

def select_kaupat(ketju):
    c.execute("SELECT * FROM kaupat WHERE ketju = ?", [ketju])
    return c.fetchall()


'''
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
'''

def kloop(kauppa, hakusana1, hakusana2):

    driver.find_element_by_xpath(
        "/html/body/div[1]/section/header/div[1]/nav/ul[1]/li[1]/a/span"
    ).click()
    driver.find_element_by_xpath(
        "/html/body/div[1]/section/header/div[1]/nav/ul[2]/div/nav/div[2]/div/span/span"
    ).click()
    driver.find_element_by_xpath(
        "/html/body/div[2]/div/div[2]/div[2]/form/div/div/input"
    ).send_keys(kauppa)
    sleep(2)
    driver.find_element_by_xpath(
        "/html/body/div[2]/div/div[2]/div[2]/div/div/a[1]/div[1]/div[2]"
    ).click()
    khaku = driver.find_element_by_xpath(
        "/html/body/div[1]/section/section/div[2]/div[1]/div/div[2]/div/div[3]/input"
    )
    khaku.clear()
    khaku.send_keys(hakusana1)
    sleep(2)
    try:
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/section/div[2]/div[2]/div/div/div/div/div/ul/li[1]/div/a"
        ).click()
        sleep(2)
        a = driver.find_element_by_xpath(
            "/html/body/div[1]/section/section/div[2]/div[2]/section/section/div/div[1]/section/section[1]/div[1]/div/div[1]/span"
        ).text
        palautus1 = " - Twelvi maksaa: " + a
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/section/div[2]/div[2]/section/section/div/div[1]/section/a"
        ).click()
    except NoSuchElementException:
        pass
        palautus1 = " - Ei myy twelviä"

    sleep(5)
    khaku.clear()
    khaku.send_keys(hakusana2)

    try:
        sleep(2)
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/section/div[2]/div[2]/div/div/div/div/div/ul/li[1]/div/a "
        ).click()
        sleep(2)
        b = driver.find_element_by_xpath(
            "/html/body/div[1]/section/section/div[2]/div[2]/section/section/div/div[1]/section/section[1]/div[1]/div/div[1]/span"
        ).text
        palautus2 = " - Sixi maksaa: " + b
    except NoSuchElementException:
        pass
        palautus2 = " - Ei myy sixiä"

    return kauppa + palautus1 + palautus2


def sloop(kauppa, hakusana1, hakusana2):

    d.find_element_by_xpath(
        "/html/body/div[5]/div[2]/header/div[3]/div/div[1]/div/nav/ul/li[4]/div/a/span"
    ).click()
    sleep(5)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(kauppa)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(Keys.ENTER)
    sleep(5)
    d.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div[7]/div/div[3]/div[2]/div/ul/li[1]/div[1]/div[1]/a[2]"
    ).click()
    sleep(5)
    d.find_element_by_xpath(
        "/html/body/div[5]/div[2]/header/div[2]/div/div/div/div/a"
    ).click()
    sleep(5)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(hakusana1)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(Keys.ENTER)
    sleep(5)
    try:
        sleep(5)
        d.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div[7]/div/div[2]/div[2]/div/div[3]/ul/li/a/div/img"
        ).click()
        sleep(5)
        a = (
            d.find_element_by_xpath(
                "/html/body/div[7]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/span[1]"
            ).text
            + ","
            + d.find_element_by_xpath(
                "/html/body/div[7]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/span[2]"
            ).text
        )
        d.find_element_by_xpath(
            "/html/body/div[7]/div/div/div/div[1]/button/span[1]"
        ).click()
        palautus1 = " - Twelvi maksaa: " + a

    except NoSuchElementException:
        pass
        palautus1 = " - Ei myy twelviä"

    sleep(2)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').clear()
    sleep(2)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(hakusana2)
    sleep(2)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(Keys.ENTER)
    sleep(2)

    try:
        d.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div[7]/div/div[2]/div[2]/div/div[3]/ul/li/a/div/img"
        ).click()
        sleep(5)
        x = d.find_element_by_xpath(
            "/html/body/div[7]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/span[1]"
        ).text
        y = d.find_element_by_xpath(
            "/html/body/div[7]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/span[2]"
        ).text
        d.find_element_by_xpath(
            "/html/body/div[7]/div/div/div/div[1]/button/span[1]"
        ).click()
        palautus2 = " - Sixi maksaa " + x + "," + y
        sleep(1)
    except NoSuchElementException:
        pass
        palautus2 = " - Ei myy sixiä"
        sleep(1)

    return kauppa + palautus1 + palautus2

skaupat = select_kaupat("S-Ryhmä")
print(skaupat)
kkaupat = select_kaupat("Kesko")
print(kkaupat)


'''
hinta_tauluun()
'''


driver = webdriver.Firefox()
driver.get("https://www.k-ruoka.fi/")

for k in kkaupat:
    print(kloop(k[1],"Laitilan kukko 12-", "Kukko lager 6-pack"))
driver.close()

d = webdriver.Firefox()

<<<<<<< HEAD
    for s in skaupat:
        print(sloop("Laitilan kukko 12-", "Laitilan kukko lager 6-"))
    print(str(i) + "Kieppi")
=======
d.get("https://www.foodie.fi")
for s in skaupat:
    print(sloop(s[1],"Laitilan kukko 12-", "kukko lager 6-"))
>>>>>>> 4a17af2e640a41eb51c8922926ae285bdee384da


d.close()

