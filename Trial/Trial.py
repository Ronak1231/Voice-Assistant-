import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_GEMINI_KEY")

speech = sr.Recognizer()
engine = pyttsx3.init()


# Set NewsAPI Key
newsapi = "e5fedcb981d24ec6ad52b536c5385ccd"
url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={newsapi}"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    genai.configure(api_key=GOOGLE_GEMINI_KEY)

    model = genai.GenerativeModel('gemini-1.5-flash')

    system_prompt = """
    You are a virtual assistant named Jarvis. 
    You can answer general questions, assist with tasks, and behave like a helpful AI (similar to Alexa or Google Assistant).
    """

    # Use actual voice command
    user_question = command

    response = model.generate_content([system_prompt, user_question])
    print("Jarvis:", response.text)
    speak(response.text)
    return True

def processcommand(c):
   if "open google" in c.lower():
       webbrowser.open("https://www.google.com/")
       speak("opening google...")
       return True
   elif "open youtube" in c.lower():
       webbrowser.open("https://www.youtube.com/")
       speak("opening youtube...")
       return True
   elif "open linkedin" in c.lower():
       webbrowser.open("https://www.linkedin.com/")
       speak("opening linkedin...")
       return True
   elif "open facebook" in c.lower():
       speak("opening facebook...")
       webbrowser.open("https://www.facebook.com/")
       return True
   elif "open github" in c.lower():
       speak("opening github...")
       webbrowser.open("https://www.github.com/")
       return True
       
   elif "play" in c.lower():
        speak("What do you want to play?.....")

        song = input("Enter: ").lower()
        
        if song in musiclibrary.music:
            webbrowser.open(musiclibrary.music[song])
            return True
        else:
            speak("Sorry, I couldn't find that song.")
            return True



   elif "news" in c.lower():
    try:
        req = requests.get(url)
        if req.status_code == 200:
            data = req.json()
            articles = data.get('articles', [])
            
            if not articles:
                print("No articles found.")
                speak("Sorry, no news articles found.")
            else:
                speak("Number of news you want: ")
                n = int(input("Enter: "))
                print(f"Here are the top {n} headlines:\n")
                speak(f"Here are the top {n} news headlines.")
                
                for i, article in enumerate(articles[:n]):  # limit to 10
                    title = article.get('title', 'No Title')
                    source = article.get('source', {}).get('name', 'Unknown Source')
                    print(f"{i + 1}. {title} - {source}")
                    speak(f"Headline {i + 1}: {title}")
                
                # Repeatedly ask user for article until they say 'stop'
                while True:
                    speak("Which article number would you like me to read in detail? Say stop to end.")

                    try:
                        response = input("Enter: ")
                        
                        if 'stop' in response:
                            speak("Okay, stopping the news reader.")
                            return True

                        elif response.isdigit():
                            index = int(response) - 1
                            if 0 <= index < len(articles):
                                selected = articles[index]
                                print(f"\nTitle: {selected['title']}")
                                print(f"Description: {selected.get('description', 'No description')}")
                                print(f"URL: {selected.get('url')}")
                                speak("Here's more about it:")
                                speak(selected.get('description', 'No description available.'))
                            else:
                                print("Invalid selection.")
                                speak("That is an invalid selection.")
                        else:
                            speak("Invalid input. Please say a number or say stop.")
                    except sr.UnknownValueError:
                        speak("Sorry, I didn't catch that. Please repeat.")
                    except sr.WaitTimeoutError:
                        speak("I didn't hear anything. Please try again.")
        else:
            print("Failed to fetch news.")
            speak("Sorry, I couldn't fetch the news.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("An error occurred while fetching the news.")

   elif "stop" in c.lower():
        speak("Do you really want to shut me down? Say yes to confirm.")
        confirmation = input("Enter: ")
        if "yes" in confirmation:
            speak("Shutting down.")
            return False
        else:
            speak("Shutdown canceled.")    
                    
   else:
       aiprocess(c)
       return True


if __name__ == "__main__":
    speak("Initilized Javis...")
keep_running = True

while keep_running :
        try:
            print("jarvis Active.....")
            command = input("Enter: ")
            keep_running  = processcommand(command)

        except Exception as e:
            print("Error; {0}".format(e))

