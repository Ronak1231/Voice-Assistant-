import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests

speech = sr.Recognizer()
engine = pyttsx3.init()
# Set NewsAPI Key
newsapi = "e5fedcb981d24ec6ad52b536c5385ccd"
url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={newsapi}"

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

   elif "news" in c.lower():
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            
            if not articles:
                print("No articles found.")
                engine.say("Sorry, no news articles found.")
                engine.runAndWait()
            else:
                print(f"Here are the top {len(articles)} headlines:\n")
                engine.say("Here are the top news headlines.")
                engine.runAndWait()
                
                for i, article in enumerate(articles[:10]):  # limit to 10
                    title = article.get('title', 'No Title')
                    source = article.get('source', {}).get('name', 'Unknown Source')
                    print(f"{i + 1}. {title} - {source}")
                    engine.say(f"Headline {i + 1}: {title}")
                    engine.runAndWait()
                
                # Repeatedly ask user for article until they say 'stop'
                while True:
                    engine.say("Which article number would you like me to read in detail? Say stop to end.")
                    engine.runAndWait()
                    choice = input("\nEnter article number or type 'stop' to exit: ").strip().lower()

                    if choice == 'stop':
                        engine.say("Okay, stopping the news reader.")
                        engine.runAndWait()
                        break
                    elif choice.isdigit():
                        index = int(choice) - 1
                        if 0 <= index < len(articles):
                            selected = articles[index]
                            print(f"\nTitle: {selected['title']}")
                            print(f"Description: {selected.get('description', 'No description')}")
                            print(f"URL: {selected.get('url')}")

                            engine.say("Here's more about it:")
                            engine.say(selected.get('description', 'No description available.'))
                            engine.runAndWait()
                        else:
                            print("Invalid selection.")
                            engine.say("That is an invalid selection.")
                            engine.runAndWait()
                    else:
                        print("Invalid input.")
                        engine.say("Invalid input. Please enter a number or say stop.")
                        engine.runAndWait()
        else:
            print("Failed to fetch news.")
            engine.say("Sorry, I couldn't fetch the news.")
            engine.runAndWait()
    except Exception as e:
        print(f"An error occurred: {e}")
        engine.say("An error occurred while fetching the news.")
        engine.runAndWait()


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

