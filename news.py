import requests
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

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
