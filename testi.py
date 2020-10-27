import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pymysql
import sshtunnel
import MySQLdb as mysql
from threading import Thread

start = datetime.now()
date = datetime.now().strftime("%d.%m.%Y")

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

tunneli = sshtunnel.SSHTunnelForwarder(('ssh.eu.pythonanywhere.com',22), ssh_username="Leba", ssh_password="Lebalol123",
                                       remote_bind_address=("Leba.mysql.eu.pythonanywhere-services.com", 3306))
tunneli.start()
print("muip")

def novar_db_command(command):

        connection = pymysql.connect(
            user="Leba",
            password="superpassu",
            host="127.0.0.1",
            port=tunneli.local_bind_port,
            database="Leba$Kukko")


        cur = connection.cursor()
        cur.execute(command)
        try:
            result = cur.fetchall()
        except:
            result = "vituiks män"

        connection.close()
        return result


def db_command(command, variables):
        connection = pymysql.connect(
            host="127.0.0.1",
            user="Leba",
            password="superpassu",
            database="Leba$Kukko",
            port=tunneli.local_bind_port
        )

        cur = connection.cursor()
        cur.execute(command, variables)
        result = cur.fetchall()
        connection.commit()
        connection.close()
        return result


clean = lambda dirty: "".join(filter(string.printable.__contains__, dirty))


def find_element(driver, xpath):
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath,))
    )
    return element


def ei_kkaupassa(driver, xpath):
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, xpath,))
    )
    return element


def ei_skaupassa(driver, xpath):
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, xpath,))
    )
    return element


def find_ruksi(driver, xpath):
    element = WebDriverWait(driver, 30).until(
        (EC.element_to_be_clickable((By.XPATH, xpath)))
    )
    return element


def create_kauppa():
    command = "CREATE TABLE IF NOT EXISTS kauppa ( id INT AUTO_INCREMENT PRIMARY KEY, nimi TEXT, ketju TEXT)"
    novar_db_command(command)


def create_tuote():
    command = "CREATE TABLE IF NOT EXISTS tuote (id INT AUTO_INCREMENT PRIMARY KEY, nimi TEXT, yksiköt TEXT, viivakoodi TEXT)"
    novar_db_command(command)


def create_hintaKaupassa():
    command = "CREATE TABLE IF NOT EXISTS hintaKaupassa ( id INT AUTO_INCREMENT PRIMARY KEY, tuote_id INTEGER, kauppa_id INTEGER, hinta DECIMAL(4,2), paivays TEXT, FOREIGN KEY(tuote_id) REFERENCES tuote(id), FOREIGN KEY(kauppa_id) REFERENCES kauppa(id))"
    novar_db_command(command)


def create_hinta_historia():
    command = "CREATE TABLE IF NOT EXISTS hintaHistoria (id INT AUTO_INCREMENT PRIMARY KEY, tuote_id INTEGER, kauppa_id INTEGER, hinta TEXT, alkupvm TEXT, FOREIGN KEY(tuote_id) REFERENCES tuote(id), FOREIGN KEY(kauppa_id) REFERENCES kauppa(id))"
    novar_db_command(command)


def insert_tuote(nimi, nro, viivakoodi):
    sql = "INSERT INTO tuote (nimi, yksiköt, viivakoodi) VALUES (%s,%s,%s)"
    db_command(sql, (nimi, nro, viivakoodi))


def insert_kaupat(kauppa, ketju):
    command = "INSERT INTO kauppa (nimi, ketju) VALUES (%s, %s)"
    db_command(command, (kauppa, ketju))


def hinta_tauluun(tuote_id, kauppa_id, hinta, date, kappalehinta):
    sql = "INSERT INTO hintaKaupassa (tuote_id, kauppa_id, hinta, paivays, kappalehinta) VALUES (%s,%s,%s,%s, %s)"
    db_command(sql, (tuote_id, kauppa_id, hinta, date, kappalehinta))


def select_kaupat(ketju):
    sql = "SELECT * FROM kauppa WHERE ketju = %s"
    return db_command(sql, [ketju])


def get_tuotteet():
    sql = "SELECT * FROM tuote"
    return novar_db_command(sql)


def get_hinta(tuote_id, kauppa_id):
    sql = "SELECT * FROM hintaKaupassa WHERE tuote_id = %s AND kauppa_id = %s"
    return db_command(sql, (tuote_id, kauppa_id))


def update_hinta(tuote_id, kauppa_id, hinta, date, kappalehinta):
    sql = "UPDATE hintaKaupassa SET hinta = %s, paivays = %s, kappalehinta = %s WHERE tuote_id = %s AND kauppa_id = %s"
    return db_command(sql, (hinta, date, kappalehinta, tuote_id, kauppa_id))


def insert_historia(tuote_id, kauppa_id, hinta, date):
    sql = "INSERT INTO hintaHistoria (tuote_id, kauppa_id, hinta, alkupvm) VALUES (%s,%s,%s,%s)"
    return db_command(sql, (tuote_id, kauppa_id, hinta, date))


def hintavertailu(tuote_id, kauppa_id, hinta_nyt, kappalehinta):
    if len(get_hinta(tuote_id, kauppa_id)) == 0:
        hinta_tauluun(tuote_id, kauppa_id, hinta_nyt, date, kappalehinta)
    else:
        get = get_hinta(tuote_id, kauppa_id)[0]
        hist_hinta = get[3]
        hist_pvm = get[4]
        print(
            "Kantaan lähtee: TuoteID: "
            + str(tuote_id)
            + ", KauppaID: "
            + str(kauppa_id)
            + ", hinta: "
            + str(hinta_nyt)
            + "ja kappalehinta: "
            + str(kappalehinta),
        )
        # insert_historia(tuote_id, kauppa_id, hist_hinta, hist_pvm)
        update_hinta(tuote_id, kauppa_id, hinta_nyt, date, kappalehinta)


def find_substring(list, substring):
    for l in list:
        if substring in l:
            return l


def sloop(d, skauppa):
    print("Dasd")
    e = find_element(d, "/html/body/div[5]/div[2]/header/div[3]/div/div[1]/div/nav/ul/li[4]/div/a/span", )
    e.click()
    sleep(5)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(skauppa[1])
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(Keys.ENTER)
    e = find_element(
        d,
        "/html/body/div[5]/div[2]/div[7]/div/div[3]/div[2]/div/ul/li[1]/div[1]/div[1]/a[2]",
    )
    e.click()
    e = find_element(d, "/html/body/div[5]/div[2]/header/div[2]/div/div/div/div/a")
    e.click()
    sleep(5)
    for t in tuotteet:
        d.get("https://www.foodie.fi/entry/" + t[3])
        soppa = BeautifulSoup(d.page_source, 'html.parser')

        try:
            divi = soppa.find("div", {"class": "prices"})
            hinta1 = divi.find("span", {"class": "whole-number"}).text
            hinta2 = divi.find("span", {"class": "decimal"}).text
            hinta = hinta1 + "." + hinta2
            thread = Thread(target=hintavertailu, args=(t[0], skauppa[0], hinta, round(float(hinta) / int(t[2]), 2)))
            thread.start()

        except AttributeError:
            thread = Thread(target=hintavertailu, args=(t[0], skauppa[0], 99.99, 99.99))
            thread.start()


def kloop(driver, kkauppa):
    e = find_element(
        driver, '//*[@id="open-store-menu"]/a/span'
    )
    e.click()
    e = find_element(
        driver,
        '//*[@id="store-menu"]/div[2]/div/span',
    )
    e.click()
    sleep(3)
    e = find_element(driver, '//*[@id="store-selector-modal"]/div[3]/form/div/div/input')
    e.send_keys(kkauppa[1])
    sleep(3)
    e = find_element(
        driver, '//*[@id="store-selector-modal"]/div[3]/div/div/a/div[1]')
    e.click()
    sleep(3)
    for t in tuotteet:
        find_substring(linkit, t[3])
        driver.get(find_substring(linkit, t[3]))
        sleep(2)
        soppa = BeautifulSoup(driver.page_source, 'html.parser')
        hinta = soppa.find("span", {"class": "price"}).text
        korjattu = hinta.replace(',', '.')
        if "€" in hinta or "/kpl" in hinta:
            thread = Thread(target=hintavertailu, args=(t[0], kkauppa[0], 99.99, 99.99))
            thread.start()
        else:
            thread = Thread(target=hintavertailu, args=(t[0], kkauppa[0], korjattu, round(float(korjattu) / int(t[2]), 2)))
            thread.start()


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

kaupat = select_kaupat("Kesko")
skaupat = select_kaupat("S-Ryhmä")
tuotteet = get_tuotteet()

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
driver.get("https://www.k-ruoka.fi/")
driver.find_element_by_xpath('//*[@id="kconsent"]/div/div/div[2]/div[3]/div[1]/button[2]').click()

for k in kaupat:
    kloop(driver, k)
driver.close()

d = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
d.get("https://www.foodie.fi")
e = find_element(d, "/html/body/div[8]/div/div[2]/div/button[1]")
e.click()
sleep(2)

for skau in skaupat:
    sloop(d, skau)
d.close()
print("Skriptin kesto: " + str(datetime.now() - start))
sleep(15)
tunneli.close()

