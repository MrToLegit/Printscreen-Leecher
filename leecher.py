from urllib.request import Request, urlopen
import random
import string
from time import sleep
import webbrowser
from pathlib import Path
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

scanned = []

def writeoutput():
    if os.path.isfile(os.path.realpath(__file__) + "/output.txt"):
        os.remove(os.path.realpath(__file__) + "/output.txt")
    f=open(os.path.realpath(__file__) + "/output.txt", "a+")
    for s in scanned:
        f.write(s + "\n")


maxscanns = input("Enter how much scans do you want do run: ")
openweb = input("Do you want to open automatically the links? [y/n]: ")

while openweb != "y" and openweb != "n":
    openweb = input("Do you want to open automatically the links? [y/n]: ") 

saveoutput = input("Do you want to open automatically the links? [y/n]: ")

while saveoutput != "y" and saveoutput != "n":
    saveoutput = input("Do you want to save the founded links? [y/n]: ") 

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

for i in range(int(maxscanns), 0, -1):
    sleep(0.001)
    link = "https://prnt.sc/"+id_generator()
    if not link in scanned:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode("utf8")


        driver.get(link)
        try:
            org = driver.find_element_by_id('screenshot-image')
            # Find the value of org?
            val = org.get_attribute("src")
            if not ".png" in val:
                continue
        except:
            print("Not Found: " + link)

        if '<div class="under-image">' in webpage:
            if openweb == "y" or openweb == "Y":
                webbrowser.open_new_tab(val)
            print(val)
            scanned.append(val)
            if saveoutput == "y" or saveoutput == "Y":
                writeoutput()