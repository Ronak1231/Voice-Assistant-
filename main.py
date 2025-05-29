import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests

speech = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "e5fedcb981d24ec6ad52b536c5385ccd"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def processcommand(c):
   if "open google" in c.lower():
       webbrowser.open("https://www.google.com/")
       speak("opening google...")
   elif "open youtube" in c.lower():
       webbrowser.open("https://www.youtube.com/")
       speak("opening youtube...")
   elif "open linkedin" in c.lower():
       webbrowser.open("https://www.linkedin.com/")
       speak("opening linkedin...")
   elif "open facebook" in c.lower():
       speak("opening facebook...")
       webbrowser.open("https://www.facebook.com/")
   elif "open github" in c.lower():
       speak("opening github...")
       webbrowser.open("https://www.github.com/")
       
   elif "play song" in c.lower():
        # r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("What do you want to play?.....")
            audio = speech.listen(source, timeout=2, phrase_time_limit= 1)
                
            song = speech.recognize_google(audio).strip().lower()
            link = musiclibrary.music[song]
            webbrowser.open(link)

#    elif "news" in c.lower():
#         r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
#         if r.status_code == 200:
#             # Parse the JSON response
#             data = r.json()
            
#             # Extract the articles
#             articles = data.get('articles', [])
            
#             # Print the headlines
#             for article in articles:
#                 speak(article['title'])

   elif "stop" in c.lower():
        speak("Shutting down.")
        return False
                    
   else:
       pass



if __name__ == "__main__":
    speak("Initilized Javis...")
keep_running = True

while keep_running :
        r = sr.Recognizer()
        
        print("Recognizing....")

        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listining.....")
                audio = r.listen(source, timeout=5, phrase_time_limit= 3)
            word = r.recognize_google(audio)
            speak(word)
            if(word.lower() == "jarvis"):
                speak("Yes? ")
                with sr.Microphone() as source:
                    print("jarvis Active.....")
                    # r.adjust_for_ambient_noise(source, duration=1)
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    keep_running  = processcommand(command)



        except Exception as e:
            print("Error; {0}".format(e))

