from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import sqlite3
from selenium.common.exceptions import NoSuchElementException
import datetime
import string

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

conn = sqlite3.connect("kukko.db")
c = conn.cursor()


def create_kauppa():
    c.execute(
        "CREATE TABLE IF NOT EXISTS kauppa ( id INTEGER PRIMARY KEY, nimi TEXT, ketju TEXT)"
    )


def create_tuote():
    c.execute(
        "CREATE TABLE IF NOT EXISTS tuote (id INTEGER PRIMARY KEY, nimi TEXT, yksiköt TEXT, k_hakusana TEXT, s_hakusana TEXT)"
    )


def create_hintaKaupassa():
    c.execute(
        "CREATE TABLE IF NOT EXISTS hintaKaupassa ( id INTEGER PRIMARY KEY, tuote_id INTEGER, kauppa_id INTEGER, hinta TEXT, paivays TEXT, FOREIGN KEY(tuote_id) REFERENCES tuote(id), FOREIGN KEY(kauppa_id) REFERENCES kauppa(id))"
    )


def create_hinta_historia():
    c.execute(
        "CREATE TABLE IF NOT EXISTS hintaHistoria ( id INTEGER PRIMARY KEY, tuote_id INTEGER, kauppa_id INTEGER, hinta TEXT, alkupvm TEXT, FOREIGN KEY(tuote_id) REFERENCES tuote(id), FOREIGN KEY(kauppa_id) REFERENCES kauppa(id))"
    )


def insert_tuote(nimi, nro, khaku, shkau):
    sql = "INSERT INTO tuote (nimi, yksiköt, k_hakusana, s_hakusana) VALUES (?,?,?,?)"
    c.execute(sql, (nimi, nro, khaku, shkau))
    conn.commit()


def insert_kaupat(kauppa, ketju):
    c.execute("INSERT INTO kauppa (nimi, ketju) VALUES (?, ?)", (kauppa, ketju))
    conn.commit()


def hinta_tauluun(tuote_id, kauppa_id, hinta, date):
    sql = "INSERT INTO hintaKaupassa (tuote_id, kauppa_id, hinta, paivays) VALUES (?,?,?,?)"
    c.execute(sql, (tuote_id, kauppa_id, hinta, date))
    conn.commit()


def select_kaupat(ketju):
    c.execute("SELECT * FROM kauppa WHERE ketju = ?", [ketju])
    return c.fetchall()


def get_tuotteet():
    c.execute("SELECT * FROM tuote")
    return c.fetchall()


def get_hinta(tuote_id, kauppa_id):
    sql = "SELECT * FROM hintaKaupassa WHERE tuote_id = ? AND kauppa_id = ?"
    c.execute(sql, (tuote_id, kauppa_id))
    return c.fetchall()


def update_hinta(tuote_id, kauppa_id, hinta, date):
    sql = "UPDATE hintaKaupassa SET hinta = ?, paivays = ? WHERE tuote_id = ? AND kauppa_id = ?"
    c.execute(sql, (hinta, date, tuote_id, kauppa_id))
    conn.commit()


def insert_historia(tuote_id, kauppa_id, hinta, date):
    sql = "INSERT INTO hintaHistoria (tuote_id, kauppa_id, hinta, alkupvm) VALUES (?,?,?,?)"
    c.execute(sql, (tuote_id, kauppa_id, hinta, date))
    conn.commit()


def hintavertailu(tuote_id, kauppa_id, hinta_nyt):
    print("#" * 50)

    if len(get_hinta(tuote_id, kauppa_id)) == 0:
        hinta_tauluun(tuote_id, kauppa_id, hinta_nyt, date)
    elif str(hinta_nyt).strip() == str(get_hinta(tuote_id, kauppa_id)[0][3]).strip():
        print("Sama hinta ei toimita")
        print(str(hinta_nyt).strip())
        print(str(get_hinta(tuote_id,kauppa_id)[0][3]).strip())
    else:
        print(str(tuote_id), " + " + str(kauppa_id))
        get = get_hinta(tuote_id, kauppa_id)[0]
        hist_hinta = get[3]
        hist_pvm = get[4]
        insert_historia(tuote_id, kauppa_id, hist_hinta, hist_pvm)
        update_hinta(tuote_id, kauppa_id, hinta_nyt, date)
        print("Hinta muuttunut:")
        print(get_hinta(tuote_id, kauppa_id)[0][3])
        print(hinta_nyt)


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

def kloop(kauppa, kauppa_id, tuotteet):

    driver.find_element_by_xpath(
        "/html/body/div[1]/section/header/div[1]/nav/ul[1]/li[1]/a/span"
    ).click()
    driver.find_element_by_xpath(
        "/html/body/div[1]/section/header/div[1]/nav/ul[2]/div/nav/div[2]/div/span/span"
    ).click()
    driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/form/div/div/input").send_keys(kauppa)
    sleep(5)
    driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/a[1]/div[1]/div[2]").click()
    khaku = driver.find_element_by_xpath("/html/body/div[1]/section/section/div[2]/div[1]/div/div[2]/div/div[3]/input")
    for t in tuotteet:
        try:
            khaku.clear()
            sleep(2)
            khaku.send_keys(t[3])
            sleep(5)

            driver.find_element_by_xpath("/html/body/div[1]/section/section/div[2]/div[2]/div/div/div/div/div/ul/li[1]/div/a").click()
            sleep(5)
            a = driver.find_element_by_xpath("/html/body/div[1]/section/section/div[2]/div[2]/section/section/div/div[1]/section/section[1]/div[1]/div/div[1]/span").text
            driver.find_element_by_xpath("/html/body/div[1]/section/section/div[2]/div[2]/section/section/div/div[1]/section/a").click()
            hintavertailu(t[0], kauppa_id, clean(a))

        except NoSuchElementException:
            pass
            a = "Ei valikoimassa"
            hintavertailu(t[0], kauppa_id, clean(a))



def sloop(kauppa, kauppa_id, tuotteet):

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
    for t in tuotteet:
        d.find_element_by_xpath('//*[@id="multisearch-query"]').clear()
        d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(t[4])
        d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(Keys.ENTER)
        sleep(5)
        try:
            sleep(7)
            d.find_element_by_xpath("/html/body/div[5]/div[2]/div[7]/div/div[2]/div[2]/div/div[3]/ul/li/a/div/img").click()
            sleep(5)
            a = (
                d.find_element_by_xpath(
                    "/html/body/div[7]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/span[1]").text+ ","+ d.find_element_by_xpath(
                    "/html/body/div[7]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/span[2]").text)
            sleep(8)
            d.find_element_by_xpath(
                "/html/body/div[7]/div/div/div/div[1]/button/span[1]"
            ).click()
            sleep(4)
            hintavertailu(t[0], kauppa_id,clean(a))

        except NoSuchElementException:
            pass
            a = "Ei valikoimassa"
            hintavertailu(t[0], kauppa_id, clean(a))
            sleep(4)

date = datetime.datetime.now().strftime("%d.%m.%Y")
skaupat = select_kaupat("S-Ryhmä")
kkaupat = select_kaupat("Kesko")
tuotteet = get_tuotteet()

driver = webdriver.Firefox()
driver.get("https://www.k-ruoka.fi/")

for k in kkaupat:
    kloop(k[1], k[0], tuotteet)

driver.close()

d = webdriver.Firefox()
d.get("https://www.foodie.fi")
for s in skaupat:
    sloop(s[1], s[0], tuotteet)

d.close()
