from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sqlite3
import telebot

chrome_options = Options()
chrome_options.add_argument("-headless")
nav = webdriver.Chrome(options=chrome_options)

nav.get('https://blaze.com/pt/games/double')
tfg = []
i = 1
while i <= 6:
    pegardados = nav.find_element(By.XPATH, f'//*[@id="roulette-recent"]/div/div[1]/div[{i}]').text
    if pegardados != '':
        tfg.append(pegardados)
    else:
        tfg.append('0')
    i += 1
print(tfg)
"""
//*[@id="roulette-recent"]/div/div[1]/div[10]/div/div/img
"""


nav.quit()
