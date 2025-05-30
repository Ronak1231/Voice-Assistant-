from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_GEMINI_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_GEMINI_KEY)

# Initialize Gemini model (valid one from your list)
model = genai.GenerativeModel('gemini-1.5-flash')

# Define system instruction
system_prompt = """
You are a virtual assistant named Jarvis. 
You can answer general questions, assist with tasks, and behave like a helpful AI (similar to Alexa or Google Assistant).
"""

# User input
user_question = "What is coding?"

# Get response from Gemini
response = model.generate_content([system_prompt, user_question])

# Output response
print("Jarvis:", response.text)
