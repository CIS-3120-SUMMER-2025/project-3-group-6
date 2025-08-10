import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    print("Warning: WEATHER_API_KEY not found in environment variables.")
    print("Please create a .env file with your WEATHER_API_KEY.")
    
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama") 
WEATHER_URL = "https://api.weatherapi.com/v1/current.json"

def get_weather(city):
    if not WEATHER_API_KEY:
        return "API key not found."
    try:
        response = requests.get(
            WEATHER_URL,
            params={"key": WEATHER_API_KEY, "q": city, "aqi": "no"},
        )
    except Exception as e:
        return "Request failed"
    if response.status_code != 200:
        return "Weather API error"
    data = response.json()
    return {
        "location": f"{data['location']['name']}, {data['location']['region'] or data['location']['country']}",
        "temp_f": data["current"]["temp_f"],
        "condition": data["current"]["condition"]["text"],
    }


def build_weather_prompt(piece_type, city, weather):
    if piece_type == "short story":
        guide = "Write a short story."
    elif piece_type == "journal":
        guide = "Write a journal entry."
    else:
        guide = "Write a poem."
    header = f"City: {city}\nWeather: {weather['condition']}, {weather['temp_f']}°F in {weather['location']}\n"
    rules  = f"Use the local weather as atmosphere and influence on mood and actions. Return only the {piece_type}.\n"
    return guide + "\n" + header + rules


def call_ollama(prompt_text):
    try:
        r = requests.post(
            OLLAMA_HOST.rstrip("/") + "/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt_text, "stream": False}
        )
        if r.status_code == 200:
            return r.json().get("response", "").strip()
        return "Error"
    except Exception as e:
        return "Ollama not reachable" 

def build_app():
    with gr.Blocks(title="Weather Mood Writer") as demo:
        gr.Markdown("Weather Mood Writer")
        gr.Markdown("Choose a city, then select a writing mode to generate a creative writing based on current weather conditions.")

        city = gr.Textbox(placeholder="City", show_label=False)
        piece_type = gr.Dropdown(["short story", "journal", "poem"], show_label=False)
        generate_btn = gr.Button("Generate")
        output_box = gr.Textbox(lines=16, show_label=False, placeholder="Result will appear here")

        def generate_handler(ptype, city_name):
            weather = get_weather(city_name)
            if not isinstance(weather, dict):
                return weather
            prompt = build_weather_prompt(ptype, city_name, weather)
            model_output = call_ollama(prompt)
            return f"[{weather['location']}, {weather['temp_f']}°F, {weather['condition']}]\n\n{model_output}"

        generate_btn.click(generate_handler, inputs=[piece_type, city], outputs=[output_box])
    return demo


app = build_app()
app.launch()
