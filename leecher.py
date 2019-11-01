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
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import sys
import threading
import winsound

version = "1.0"


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


scanned = []

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


# GUI START
def center(self):
    frameGm = self.frameGeometry()
    screen = QApplication.desktop().screenNumber(
        QApplication.desktop().cursor().pos())
    centerPoint = QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    self.move(frameGm.topLeft())


app = QApplication(sys.argv)

w = QWidget()
w.resize(300, 200)
center(w)

def quitprogram():
    app.quit
    quit()
    driver.service.stop()

btn = QPushButton('Quit', w)
btn.clicked.connect(lambda: quitprogram())
btn.resize(btn.sizeHint())
btn.move(w.width() / 2 - btn.width()/2, w.height() - 35)

btnsave = QPushButton('Start Leecher', w)
btnsave.clicked.connect(lambda: onclickstartleecher())
btnsave.resize(btnsave.sizeHint())
btnsave.move(w.width() / 2 - btnsave.width()/2, 105)

btnload = QPushButton('Stop Leecher', w)
btnload.clicked.connect(lambda: onclickstopleecher())
btnload.resize(btnload.sizeHint()) 
btnload.move(w.width() / 2 - btnload.width()/2, 135) 
btnload.setEnabled(False)

label = QLabel('Enter scans amount:', w)
label.resize(120,20)
label.move(w.width() / 2 - label.width()/2, 5) 

scansinput = QLineEdit(w)
scansinput.resize(120, 20)
scansinput.move(w.width() / 2 - scansinput.width()/2, 30) 
rx = QtCore.QRegExp("[0-9_]+")
scansinput.setValidator(QtGui.QRegExpValidator(rx))
scansinput.setMaxLength(2)

checkbox = QCheckBox('Open in Browser', w)
checkbox.resize(120, 20)
checkbox.move(w.width() / 2 - checkbox.width()/2, 55) 
checkbox.setChecked(1)

saveoutput = QCheckBox('Save output', w)
saveoutput.resize(120, 20)
saveoutput.move(w.width() / 2 - saveoutput.width()/2, 75) 
saveoutput.setChecked(1)

label1 = QLabel('© 2019 by ToLegit', w)
label1.resize(label1.sizeHint())
label1.move(2, w.height() - 19) 

label2 = QLabel('Public Version ' + version, w)
label2.resize(label2.sizeHint())
label2.move(w.width() - label2.width() - 2, w.height() - 19) 

def startleecher(arg):
    for i in range(int(scansinput.text()), 0, -1):
        t = threading.currentThread()
        if not getattr(t, "do_run", True):
            break
        sleep(0.001)
        link = "https://prnt.sc/"+id_generator()
        if not link in scanned:
            try:
                driver.get(link)
                org = driver.find_element_by_id('screenshot-image')
                # Find the value of org?
                val = org.get_attribute("src")
                if not ".png" in val:
                    continue
                if ".png" in val:
                    if checkbox.isChecked():
                        webbrowser.open_new_tab(val)
                    print(val)
                    scanned.append(val)
            except:
                print("Not Found: " + link)
    btnsave.setEnabled(True)
    sleep(0.1)
    btnload.setEnabled(False)
    btn.setEnabled(True)

    if saveoutput.isChecked():
        f = open(str(Path.home()) + "\\Desktop\\output.txt", "+a")
        for s in scanned:
            f.write(s + "\n")
        print("Output file saved. '"+str(Path.home()) + "\\Desktop\\output.txt"+"'")

threadleecher = None

def onclickstartleecher():
    if scansinput.text() != "" and int(scansinput.text()) <= 50:
        global threadleecher
        threadleecher = threading.Thread(target=startleecher, args=("task",))
        threadleecher.start()
        btnsave.setEnabled(False)
        sleep(0.1)
        btnload.setEnabled(True)
        btn.setEnabled(False)
    else:
        print("No scan number found or number is to big!")
        scansinput.setFocus(True)

def onclickstopleecher():
    threadleecher.do_run = False
    threadleecher.join()
    btnload.setEnabled(False)
    sleep(0.2)
    btnsave.setEnabled(True)
    btn.setEnabled(True)


w.setWindowTitle('Prnt.sc Leecher v' + version)
w.setFixedSize(w.size())
w.show()

sys.exit(app.exec_())