#!/usr/bin/env python3

# THIS WAY OF OBTAINING WALLET INFORMATION IS NOW DEPRECATED

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True

# Setup webdriver
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)  # Optional argument, if not specified will search path
wallet = "PUT YOUR WALLET ADDRESS HERE"
explorer_url = "https://www.navexplorer.com/address/" + wallet

# Get data from navexplorer
driver.get(explorer_url)
wallet_data = driver.find_elements_by_xpath("//td[@class='text-right']")
amount_received = wallet_data[2].text
donations = wallet_data[3].text
index = amount_received.find("txs") + 4
coffees = int(int(amount_received[index:-4]) / 5)

# Write new data
coffees_file = open("/home/pi/Documents/coffees_donated.txt", "w")
coffees_file.write(str(coffees))
coffees_file.close()

donations_file = open("/home/pi/Documents/donations.txt", "w")
donations_file.write(str(donations))
donations_file.close()

driver.quit()
