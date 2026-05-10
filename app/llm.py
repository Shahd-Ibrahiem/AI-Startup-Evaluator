from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# THIS LINE IS CRITICAL: It tells Python to look for the .env file
load_dotenv()
# Initialize the Google Gemini model
# We use gemini-2.5-flash as it is fast, cost-effective, and excellent for tool calling.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,  # Keep at 0 for analytical, deterministic outputs
    max_retries=2,
)