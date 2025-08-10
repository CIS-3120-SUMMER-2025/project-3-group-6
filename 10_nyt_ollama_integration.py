# Save as 10_nyt_ollama_integration.py
import gradio as gr
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get API key from environment
NYT_API_KEY = os.getenv("NYT_API_KEY")
if not NYT_API_KEY:
    print("Warning: NYT_API_KEY not found in environment variables.")
    print("Please create a .env file with your NYT API key.")

# Global variable to store current articles
current_articles = []

def get_top_stories(section="home"):
    