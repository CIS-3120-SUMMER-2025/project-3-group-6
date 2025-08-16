# project-3-group-6
AI-Enhanced Web App

*Project Instructions: 
- This project creates a web application that combines external data collected by using a weather API, Generative AI (Ollama), and an interactive UI using Gradio. The goal of this project is to gain experience in collecting and processing real-world data from a public API, and learning how to integrate Generative AI models (Ollama) into the application workflow.

*Set-up Guide: 
- Change .env file to own API key
- Run weathermoodgenai.py file
- Follow the clickthrough link(or use public one pasted below)
- Enter a city that you want to get the weather info for
- Select one of the following writing forms from a drop-down menu: short story, journal, or poem
- Click generate to obtain your Weather mood-based writing

Code changes for public link:
-app.launch()
+ app.launch(share=True, debug= True)
