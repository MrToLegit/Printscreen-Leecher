from urllib.request import Request, urlopen
import random
import string
from time import sleep
import webbrowser
from pathlib import Path
import os


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

scanned = []

def writeoutput():
    if os.path.isfile(str(Path.home()) + "/Desktop/output.txt"):
        os.remove(str(Path.home()) + "/Desktop/output.txt")
    f=open(str(Path.home()) + "/Desktop/output.txt", "a+")
    for s in scanned:
        f.write(s + "\n")


maxscanns = input("Enter how much scans do you want do run: ")

for i in range(int(maxscanns), 0, -1):
    sleep(0.001)
    link = "https://prnt.sc/"+id_generator()
    if not link in scanned:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode("utf8")

        if '<div class="under-image">' in webpage:
            webbrowser.open_new_tab(link)
            print(link)
            scanned.append(link)
            writeoutput()