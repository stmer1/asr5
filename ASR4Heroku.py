# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 12:03:39 2021

@author: jmami
"""


import speech_recognition as sr 
from gtts import gTTS
from playsound import playsound
import os
import wavio as wv 
import sys


# import required libraries 
import sounddevice as sd  
import numpy as np


# Sampling frequency 
freq = 16000

# Recording duration 
duration = 1
flag=True

while flag:
    # Start recorder with the given values 
    # of duration and sample frequency
    recarr=np.transpose(np.array([[0],[0]]))
    sndarr=np.transpose(np.array([[0],[0]]))
    thold = 0.02
    
    flag=True  #no audio yet
    while np.max(recarr[:,0])<thold:
        for i in range(200): 
            # print(i)
            recording = sd.rec(int(duration * freq), 
        				samplerate=freq, channels=2) 
            sd.wait()
            recarr=np.concatenate((recarr,recording))
            # if np.max(recording[:,0])>thold:
                # sndarr=np.concatenate((sndarr,recording))
            # check for 1 s pause
            t1sec=int(freq)
            if (i>2 and np.max(recording[:,0])<thold):
                break
    
    # Record audio for the given number of seconds 
    sd.wait()   
    
    # Convert the NumPy array to audio file 
    # wv.write("recording1.wav", recarr, freq, sampwidth=2)
    wv.write("praat_out.wav", recarr, freq, sampwidth=2)
  
    
    
    r = sr.Recognizer()
    
    # audio=sr.AudioFile("glasses1.wav")
    # audio=sr.AudioFile("recording0.wav")
    audio=sr.AudioFile("praat_out.wav")
    
    
    with audio as source:
      audio_file = r.record(source)
    try:
        result_google = r.recognize_google(audio_file)
        mywords=result_google
      #  result_ibm = r.recognize_ibm(audio_file,"apikey",'LRe5UvZaK4W0nshNIxe2-3cTLEDncpjCnmrceSIormUT')
       # mywords=result_ibm
        # print(result_google,result_ibm)
        
        # exporting the result 
  #      with open('recognized.txt',mode ='w') as file: 
   #        file.write("Recognized Speech:") 
  #         file.write("\n") 
   #        file.write(mywords['alternative'][0]['transcript']) 
           # print("ready!")
        
       # mywords = result_google['alternative'][0]['transcript']
       # print(mywords)
        if (mywords=='bye-bye' or mywords=='bye bye' or mywords=='Popeye') :
            tts=gTTS(mywords)
            tts.save('temp.mp3')
            playsound('temp.mp3')
            os.remove('temp.mp3')
            flag=False
            break
            sys.exit()
        tts=gTTS(mywords)
        tts.save('temp.mp3')
        # 
        playsound('temp.mp3')
        os.remove('temp.mp3')
    except:
        mywords = 'I could not understand. Please try again'
        tts=gTTS(mywords)
        tts.save('temp.mp3')
        playsound('temp.mp3')
        os.remove('temp.mp3')
    
