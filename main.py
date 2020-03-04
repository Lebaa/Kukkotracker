from selenium import webdriver
from time import sleep

from selenium.common.exceptions import NoSuchElementException

kaupat = ['Palokka', 'Keljo', 'Seppälä', 'Kotikenttä', 'Lutakko', 'Länsiväylä', 'Ainola', 'Aittorinne', 'Kotiväylä', 'K-Market Kuokkalanpelto', 'Schaumanin puistotie',
          'K-Market Torikeskus']


driver = webdriver.Firefox()
driver.get("https://www.k-ruoka.fi/")


def loop(hakusana):

        driver.find_element_by_xpath("/html/body/div[1]/section/header/div[1]/nav/ul[1]/li[1]/a/span").click()
        driver.find_element_by_xpath("/html/body/div[1]/section/header/div[1]/nav/ul[2]/div/nav/div[2]/div/span/span").click()
        driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/form/div/div/input").send_keys(k)
        sleep(2)
        driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/a[1]/div[1]/div[2]").click()
        driver.find_element_by_xpath("/html/body/div[1]/section/section/div[2]/div[1]/div/div[2]/div/div[3]/input").clear()
        driver.find_element_by_xpath("/html/body/div[1]/section/section/div[2]/div[1]/div/div[2]/div/div[3]/input").send_keys(hakusana)
        sleep(2)
        try:
            driver.find_element_by_xpath("/html/body/div[1]/section/section/div[2]/div[2]/div/div/div/div/div/ul/li[1]/div/a").click()
            sleep(2)
            a = driver.find_element_by_xpath("/html/body/div[1]/section/section/div[2]/div[2]/section/section/div/div[1]/section/section[1]/div[1]/div/div[1]/span").text
            return k + " - Hinta: " + a
        except NoSuchElementException:
            return k + " - Ei myy"


print("Twelvit: \n")
for k in kaupat:
    print(loop("Laitilan kukko 12-"))

print("Sixit: \n")
for k in kaupat:
    print(loop("Kukko lager 6-pack"))

