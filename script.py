from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

driver = webdriver.Chrome()
driver.delete_all_cookies()

signed_in = False
while not signed_in:
    driver.get("https://www.goodreads.com/user/sign_in")
    driver.find_element(by=By.CLASS_NAME, value="authPortalConnectButton").click()
    driver.find_element(by=By.NAME, value="email").send_keys("chshreeya@gmail.com")
    driver.find_element(by=By.NAME, value="password").send_keys("Books@1234")
    driver.find_element(by=By.ID, value="signInSubmit").click()
    if driver.current_url == "https://www.goodreads.com/":
        signed_in = True
    time.sleep(3)

print('signed in!\n')

while "https://www.goodreads.com/giveaway" not in driver.current_url:
    driver.get("https://www.goodreads.com/giveaway?sort=recently_listed&format=print")

print('on giveaways page!\n')

import datetime
now = datetime.datetime.now()
today = now.strftime("%B") + " " + str(now.day)
today
print('finding giveaways...')
dates = list(map(lambda x: x.text.split(" - ")[0], driver.find_elements(By.XPATH, "//article/div/div/div[@class='GiveawayMetadata__entryData']")))
while dates[-1] == today:
    driver.find_element(By.XPATH, "//div[@class='Divider Divider--contents Divider--largeMargin']/div/button").click()
    dates = list(map(lambda x: x.text, driver.find_elements(By.XPATH, "//article/div/div/div/div/div/div/div[@class='GiveawayMetadata__entryData']")))

titles = list(map(lambda x: x.text, driver.find_elements(By.XPATH, "//article/div/div[@class='BookListItem__title']/h3/strong/a")))
authors = list(map(lambda x: x.text, driver.find_elements(By.XPATH, "//article/div/div/h3/div/span/a/span[@class='ContributorLink__name']")))
descr = list(map(lambda x: x.text, driver.find_elements(By.XPATH, "//article/div/div/div/span[@class='Formatted']")))
links = list(map(lambda x: 'https://www.goodreads.com/giveaway/enter_print_giveaway/' + x.get_attribute("href").split('enter_choose_address/')[1].replace('?ref=giv_enter_cta','?address=4645032'), driver.find_elements(By.XPATH, "//div[@class='GiveawayMetadata__enterGiveawayButton']/a")))

for i in range(len(titles)):
    print(titles[i] + ' by ' + authors[i])
    print('Description: ' + descr[i])
    ans = input('\nDo you want to enter this giveaway?')
    if ans == 'y':
        driver.get(links[i])
        try:
            driver.find_element(by=By.NAME, value="entry_terms").click()
            driver.find_element(by=By.NAME, value="commit").click()
            print('entered!!')
        except:
            print('cant enter for some reason')
    print("\033[H\033[2J\n", end="")