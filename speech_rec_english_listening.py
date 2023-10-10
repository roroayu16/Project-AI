#!/usr/bin/env python
# coding: utf-8

import speech_recognition as sr
import pyttsx3
import elevenlabs
import openai
import io
import re
from pydub import AudioSegment
from pydub.playback import play

# open AI key
openai_api_key = 'YOUR_OPENAI_KEY'
engine = pyttsx3.init()

# Function to get input a voice from user
def select_language(microphone, r):
    while True:
        with microphone as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            language_choice = r.recognize_google(audio).lower()
        try:
            if "english" in language_choice or "inggris" in language_choice:
                engLang = "english"
                print("language choosen: "+engLang)
                playAudio('enLangChosen.wav')
                listen_user(microphone, r, "en-US")  # English language code
                # SpeakText("You choose "+engLang+" language")

            if "indonesia" in language_choice or "indonesian" in language_choice:
                indLang = "indonesia"
                print("bahasa yang dipilih: "+indLang)
                playAudio('idLangChosen.wav')
                listen_user(microphone, r, "id-ID") # Bahasa Indonesia language code
                # SpeakText("kamu memilih bahasa "+indLang)

            chooseLang = "please choose English or Indonesia"
            print(chooseLang)
            playAudio('enchooseLang.wav')
            playAudio('idchooseLang.wav')
            # SpeakText(chooseLang)

        except:
            eMessage = "Language not recognized. Please choose English or Bahasa Indonesia."
            print(eMessage)
            playAudio('enLangNotRec.wav')
            playAudio('idLangNotRec.wav')
            # SpeakText(eMessage)
            
        else: continue

def listen_user(microphone, r, language):
    while True:
        with microphone as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text = r.recognize_google(audio, language=language).lower()
        try:
            if "ganti" in text or "switch" in text:
                print('Bahasa dialihkan')
                break
            regEx = re.sub(r'(?<=\b\w)\s(?=\w\b)', '', text)
            result = get_response(regEx, openai_api_key)
            print(result)
            speak(result)

        except:
            if language == "id-ID":
                print('kalimat tidak dikenali')
                playAudio('idSentError.wav')

            if language == "en-US":
                print('sentences not recognized')
                playAudio('enSentError.wav')
            # SpeakText(eMessage)

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine.say(command)
    engine.runAndWait()

# Function to convert text to speech using elevenlabs
def speak(text):
    # Replace "YOUR_API_KEY" with your actual Eleven Labs API key
    elevenlabs.set_api_key("YOUR_ELEVENLABS_KEY")
    audio = elevenlabs.generate(
        text=text,
        
        voice="TxGEqnHWrfWFTfGW9XjX",    #Josh - American, deep
        # voice_id='EXAVITQu4vr4xnSDxMaL',  #Bella - American, soft
        # voice_id="21m00Tcm4TlvDq8ikWAM",  #Rachel - American, Calm

        model="eleven_multilingual_v2"
    )
    elevenlabs.play(audio)


# Function to get response from open ai
def get_response(get_input, api_key):
    print(get_input)

    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": get_input
        }]
    )

    return response.choices[0].message.content


# Function to play Audio default
def playAudio(fileLoc):
    audio = AudioSegment.from_file(fileLoc)
    play(audio)


# main Function
def main():
    r = sr.Recognizer()
    microphone = sr.Microphone()

    playAudio('enGreeting.wav')
    playAudio('idGreeting.wav')
    
    welcomeText = "Select a language: English or Bahasa Indonesia"
    print(welcomeText)
    # SpeakText(welcomeText)

    select_language(microphone, r)

if __name__ == "__main__":
    main()
