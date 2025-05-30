import requests
import pyttsx3
import speech_recognition as sr

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Set NewsAPI Key
newsapi = "e5fedcb981d24ec6ad52b536c5385ccd"
url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={newsapi}"

try:
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        articles = data.get('articles', [])
        
        if not articles:
            print("No articles found.")
            speak("Sorry, no news articles found.")
        else:
            
            # Ask user how many headlines they want
            try:
                with sr.Microphone() as source:
                    speak("How many news headlines do you want to listen to?")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    n_text = recognizer.recognize_google(audio).lower()
                    print(f"You said: {n_text}")
                    
                    # Extract number safely
                    n = int(''.join(filter(str.isdigit, n_text)))
                    n = min(n, 10)  # cap at 10
            except Exception as e:
                print(f"Could not understand number: {e}")
                speak("Sorry, I couldn't understand the number. Defaulting to 5 headlines.")
                n = 5

            print(f"\nHere are the top {n} headlines:\n")
            speak(f"Here are the top {n} news headlines.")
            
            for i, article in enumerate(articles[:n]):  # limit to 10
                title = article.get('title', 'No Title')
                source = article.get('source', {}).get('name', 'Unknown Source')
                print(f"{i + 1}. {title} - {source}")
                speak(f"Headline {i + 1}: {title}")
            
            # Repeatedly ask user for article until they say 'stop'
            while True:
                speak("Which article number would you like me to read in detail? Say stop to end.")

                with sr.Microphone() as source:
                    try:
                        speak("Listening...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        response = recognizer.recognize_google(audio).lower()
                        print(f"You said: {response}")
                        
                        if 'stop' in response:
                            speak("Okay, stopping the news reader.")
                            break
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
