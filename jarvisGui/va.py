import subprocess
from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from wikipedia.wikipedia import search
from jarvisUi import Ui_VoiceAssistant
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pyjokes
import os
from PyDictionary import PyDictionary
import json
import requests
#from bs4 import BeautifulSoup
import smtplib
import psutil
import wolframalpha
import time
from urllib.request import urlopen
import random
import ctypes
import winshell
#from twilio.rest import Client
#from clint.textui import progress

#list of possible things AI can do:
q= ['what can you do for me','what are the things you can do for me','things i can ask you','what are your abilities']
def abilities():
    speak('Here are the list of things you could ask me for')
    print(f'Here are the list of things you could ask me for :')
    print("open your favorite apps on Windows.\nPlay your local music files.\nTell you the forcast.\nemail to your friend.\nSearch in youtube.\nhumor you.\nand many more")
    speak("open your favorite apps on Windows.\nPlay your local music files.\nTell you the forcast.\nemail to your friend.\nSearch in youtube.\nhumor you.\nand many more")  

#User_Greeting = ['hello','hi','hey','good afternoon','good morning']

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
print(voices[1].id)
engine.setProperty('voice', voices[1].id)



def speak(audio):

    engine.say(audio) 

    engine.runAndWait()



def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<=15:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your voice assistant, How may I help you")

def sendEmail(to,cont):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('lakshmirajeev44@gmail.com','sandhyarajeev')
    server.sendmail("lakshmirajeev44@gmail.com",to,cont)
    server.close()


def news():
    API_TOI= "8d4e57e609074c8cb77155dbd620afa8"
    jsonObj = urlopen(f"https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey={API_TOI}")
    data = json.load(jsonObj)
    i = 1
    speak('here are some top news from Google')
    for item in data['articles']:
        print(str(i) + '. ' + item['title'] + '\n')
        print(f"{item['description']} \n {item['content']}")
        speak( item['title'])
        time.sleep(1)
        speak(item['description'])
        i +=1
        if i>3:
            break
  

coinflip = ['flip a coin','toss a coin']      
rno_bn = ["choose a number between","number between"]
def rno(q):
    if rno_bn[0] in q :
        query = q.replace(rno_bn[0],"")
        query = query.replace("and","")
        a = query.split(" ")
        a = [int(a[1]),int(a[3])]
        if a[0]>a[1]:
            n = random.randint(a[1],a[0])
                
        elif a[0]<a[1]:
            n= random.randint(a[0],a[1])
        speak(n)
        return(n)
    elif rno_bn[1] in q:
        query = q.replace(rno_bn[1],"")
        query = query.replace("and","")
        print(query)
        a = query.split(" ")
        a = [int(a[1]),int(a[3])]
        if a[0]>a[1]:
            n = random.randint(a[1],a[0])
        elif a[0]<a[1]:
            n= random.randint(a[0],a[1])
        return(n)  

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()    

    def takeCommand(self):
    #It takes microphone input from the user and returns string output

        r = sr.Recognizer()
        with sr.Microphone() as source:
          print("Listening...")
          r.pause_threshold = 1
          audio = r.listen(source)

        try:
         print("Recognizing...")    
         query = r.recognize_google(audio, language='en-in')
         print(f"User said: {query}\n")

        except Exception as e:
          # print(e)    
          print("Say that again please...")
          speak("Say that again please...")  
          return "None"
        return query     
        
        '''
        if 'what is the meaning of' in self.query:
           word = query.replace('what is the meaning of', '')
        else:
            print('can you provide the word you would like to know the meaning of?')
            speak('can you provide the word you would like to know the meaning of?')
            word = self.takeCommand().lower()    
        dictionary=PyDictionary(word)
        speak('searching')
        print('searching')
        print(dictionary.printMeanings()) #This print the meanings of all the words
        print(dictionary.getMeanings()) #This will return meanings as dictionaries
        print (dictionary.getSynonyms())
        '''
    

    def TaskExecution(self):
        #speak("Hey Lakshmi")
        wishme()
     
        while True:
          self.query=self.takeCommand().lower()

        # Logic for executing tasks based on query
          if 'wikipedia' in self.query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            self.query = self.query.replace("wikipedia", "")
            results = wikipedia.summary(self.query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)

          elif 'open youtube' in self.query:
             webbrowser.open("youtube.com")

          elif 'open google' in self.query:
             speak("What should I search on google")
             cm = self.takeCommand().lower()
             webbrowser.open(f"{cm}")

          elif 'open stackoverflow' in self.query:
             webbrowser.open("stackoverflow.com")

          elif 'open spotify' in self.query:
             webbrowser.open("spotify.com")   

          elif 'open zoom' in self.query:
              os.startfile('C:\\Users\\Lachuappu\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe')   

          elif 'joke' in self.query:
             rs=pyjokes.get_joke()
             print(rs)  
             speak(rs)

          elif 'the time' in self.query:
             strTime = datetime.datetime.now().strftime("%H:%M:%S")    
             speak(f"The time is {strTime}")    
        
          elif 'ok thank you and bye' in self.query:
             speak("Thanks for giving me your time and see you later")
             exit()
          
          
          elif 'what is the meaning of' in self.query:
            word = self.query.replace('what is the meaning of', '')
            dict=PyDictionary()
            meaning = dict.meaning(word)
            speak("searching")
            print("searching")
            print(meaning)
            speak(meaning)
          
          #elif 'temperature' in self.query:
              #search = "temperature in chennai" 
              #url = f"https://www.google.com/search?q={search}"
              #r = requests.get(url)
              #data = BeautifulSoup(r.text,"html.parser")
              #temp = data.find("div",class_="BNeawe").text
              #speak(f"current {search} is {temp}")
         
          elif 'email to' in self.query:
                try:
                    speak("what should i say?")
                    cont = self.takeCommand().lower()
                    to = "lakshmirajeev44@gmail.com"
                    sendEmail(to,cont)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("sorry unable to send")

          elif 'how are you' in self.query:
                print(f"I am fine, Thank you")
                speak("I am fine, Thank you")
                print(f"How are you")
                speak("How are you")
                p= self.takeCommand().lower()
                speak('Thats good to know')

          elif 'how much power left'in self.query:
              battery = psutil.sensors_battery()
              percentage = battery.percent
              print(f'your system have {percentage} percent battery')
              speak(f'your system have {percentage} percent battery')
              if percentage>=75:
                  speak("your may continue your work")
              elif percentage>=40  and percentage<=75:
                  speak("connect your system to charging point to charge")
              elif  percentage>=15 and percentage<=30:
                  speak("your system dont have much power please connect to charaging point")
              elif percentage<=15:
                  speak("your system have very low power please connect to charging point otherwise your system would shut down")
           
          elif "calculate" in self.query:
              
                # write your wolframalpha app_id here
                app_id = "94YR5V-UXK93HK6P9" 
                client = wolframalpha.Client(app_id)
      
                indx = self.query.split().index('calculate')
                self.query = self.query.split()[indx + 1:]
                res = client.query(' '.join(self.query))
                answer = next(res.results).text
                try:
                    print ("The answer is " + answer)
                    speak("The answer is " + answer)
                except:
                    print ("No results")

          #abilities of AI
          elif any(k in self.query for k in q):
                abilities()
    

          elif "weather" in self.query:
            api_key="45705589dd32ffd5394658ec8b048501"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the city name")
            city_name=self.takeCommand().lower()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))     

            
          elif 'news' in self.query:
                 news()


          elif 'lock windows' in self.query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()

          elif 'shutdown system' in self.query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')

          elif 'empty recycle bin' in self.query:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                speak("Recycle Bin Recycled")
        
          elif "restart" in self.query:
                subprocess.call(["shutdown", "/r"])

          elif "hibernate" in self.query or "sleep" in self.query:
                speak("Hibernating")
                subprocess.call("shutdown / h")

          elif "log off" in self.query or "sign out" in self.query:
                speak("Make sure all the application are closed before sign-out")
                time.sleep(5)
                subprocess.call(["shutdown", "/l"])

          elif "write a note" in self.query:
                speak(" What should i write")
                note = self.takeCommand().lower()
                file = open('jarvis.txt', 'w')
                speak("Should i include date and time")
                snfm = self.takeCommand().lower()
                if 'yes' in snfm or 'sure' in snfm:
                    strTime = datetime.datetime.now().strftime("% H:% M:% S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)

          elif "show note" in self.query:
                speak("Showing Notes")
                file = open("jarvis.txt", "r")
                print(file.read())
                speak(file.read())    

          elif any(a in self.query for a in coinflip):
                res = random.randint(1,2)
                time.sleep(0.4)
                print(f"{res}")
                speak(f"{res}")               

          



startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_VoiceAssistant()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../Jarvis images/gif 3.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        #timer = QTimer(self)
        #timer.timeout.connect(self.showTime)
        #timer.start(1000)
        startExecution.start()

    
app = QApplication(sys.argv)
VoiceAssistant = Main()
VoiceAssistant.show()
exit(app.exec_())
