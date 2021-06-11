import sys
import os
import google_trans_new
import enchant
#import urllib.request
import pyttsx3
#import pronouncing
import io
#import requests 

from PyQt5 import QtWidgets
from google_trans_new import google_translator

#наши окна
import start
import wordbook2
import err2
import err3
import addword
import addeds
import noth
import empty

translator = google_translator()  
dictionary = enchant.Dict("en_US")
engine = pyttsx3.init()
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', en_voice_id)
engine.setProperty('rate', 125)     
engine.setProperty('volume', 0.9) 
text = ""

class Start(QtWidgets.QMainWindow, start.Ui_Start):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.open.clicked.connect(self.wordbook)
        self.trans.clicked.connect(self.translate)
        self.say.clicked.connect(self.says)
        self.addd.clicked.connect(self.adding)


    def translate(self):
        global text, i, arrsplit
        self.info.clear()
        text = ""
        text = self.word.toPlainText()
        y=0
        if text != "":
            split = text.split()
            for word in split:
                y+=1
            arrsplit=[""]*y
            i=0
            for word in split:
                arrsplit[i] = word
                d = enchant.Dict("en_US")
                dettext = d.check(arrsplit[i])
                i+=1
                if dettext == False:
                    self.close()
                    self.next = Err2()
                    self.next.show()
            result = translator.translate(str(text).lower(),lang_src='en', lang_tgt='ru')
            result1 = translator.translate(str(text).lower(),lang_src='en',pronounce=True)
            self.info.addItem('Перевод:')
            self.info.addItem(result)
            self.info.addItem('Произношение:')
            self.info.addItems(result1)
        else:
            self.info.addItem('Нет слов для перевода')

    def wordbook(self):
        self.next=Wordbook()
        self.next.show()

    def says(self):
        if text != "":
            engine.say(text)
            engine.runAndWait()
        else:
            self.info.clear()
            self.info.addItem('Сначала переведите хотя бы одно слово')

    def adding(self):
        if 'arrsplit' in globals():
            self.close()
            self.next=Addwords()
            self.next.show()
        else:
            self.close()
            self.next = nothing()
            self.next.show()
            


class Err2(QtWidgets.QMainWindow, err2.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)

    def start(self):
        self.close()
        self.next=Start()
        self.next.show()

class Err3(QtWidgets.QMainWindow, err3.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)

    def start(self):
        self.close()
        self.next=Addwords()
        self.next.show()

class Addwords(QtWidgets.QMainWindow, addword.Ui_addword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.back.clicked.connect(self.start)
        self.all.clicked.connect(self.addall)
        self.add.clicked.connect(self.adds)
        self.slova.addItems(arrsplit)
        
    def addall(self):
        self.close()
        self.next = adde()
        self.next.show()

    def adds(self):
        item=""
        item = self.slova.currentItem()
        if item != None:
            word = item.text()
            n=0
            with io.open('words.txt', encoding='utf-8') as f:
                for line in f:
                    if item.text() in line:
                        n=1
            if n==1:
                self.next=Err3()
                self.next.show()
            else:
                f = open('words.txt','a')
                f.write(item.text())
            f.close
        else:
            self.close()
            self.next = emptys()
            self.next.show()

    def start(self):
        self.close()
        self.next=Start()
        self.next.show()

class adde(QtWidgets.QMainWindow, addeds.Ui_erradd):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        global arruse,arradd
        arruse=[]
        arradd=[]
        for n in range(len(arrsplit)):
            sl=arrsplit[n]
            buff=0
            with io.open('words.txt', encoding='utf-8') as f:
                for line in f:
                    if sl in line:
                        buff=1
            if buff==1:
                arruse.append(sl)
            else:
                f = open('words.txt','a')
                f.write(sl+"\n")
                arradd.append(sl)
            f.close
        self.inuse.addItems(arradd)
        self.added.addItems(arruse)

    def start(self):
        self.close()
        self.next=Start()
        self.next.show()

class Wordbook(QtWidgets.QMainWindow, wordbook2.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.back.clicked.connect(self.start)
        self.found.clicked.connect(self.Find)
        with open("words.txt") as f:
            array = f.readlines()
            array.sort()
        self.words.addItems(array)
        f.close
        item = self.words.currentItem()
        self.words.itemClicked.connect(self.Transl)

    def Transl(self):
        self.trans.clear()
        item = self.words.currentItem()
        wrd = item.text()
        res = translator.translate(str(wrd).lower(),lang_src='en', lang_tgt='ru')
        res1 = translator.translate(str(wrd).lower(),lang_src='en',pronounce=True) 
        self.trans.addItem('Перевод:\n')
        self.trans.addItem(res)
        self.trans.addItem('\nПроизношение:\n')
        self.trans.addItems(res1)

    def Find(self):
        usl=""
        usl=self.fw.toPlainText()
        self.words.clear()
        words = []
        for line in open('words.txt'):
            words += [w for w in line.split() if w.startswith(usl)]
        words.sort()
        self.words.addItem("Найдено слов: "+ str(len(words)) + "\n")
        self.words.addItems(words)

    def start(self):
        self.close()

class emptys(QtWidgets.QMainWindow, empty.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bckb.clicked.connect(self.start)

    def start(self):
        self.close()
        self.next=Addwords()
        self.next.show()

class nothing(QtWidgets.QMainWindow, noth.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ladno.clicked.connect(self.start)

    def start(self):
        self.close()
        self.next=Start()
        self.next.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Start()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()