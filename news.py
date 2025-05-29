import requests

API_KEY = "e5fedcb981d24ec6ad52b536c5385ccd"
URL = "https://newsapi.org/v2/top-headlines"
PARAMS = {
    'country': 'in',     # You can change to 'in' for India, 'gb' for UK, etc.
    'apiKey': API_KEY
}

response = requests.get(URL, params=PARAMS)

if response.status_code == 200:
    news_data = response.json()
    articles = news_data.get("articles", [])
    for idx, article in enumerate(articles[:5], start=1):  # show only top 5 news
        print(f"{idx}. {article['title']}")
        print(f"   {article['description']}")
        print(f"   URL: {article['url']}\n")
else:
    print("Failed to fetch news:", response.status_code)
