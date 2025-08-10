import gradio as gr
def process_text(input_text):
    # Count words, characters, and do some basic processing
    word_count = len(input_text.split())
    char_count = len(input_text)
    # Convert to uppercase as a simple transformation
    processed_text = input_text.upper()
    # Create a summary output
    summary = f"Word count: {word_count}\nCharacter count: {char_count}"
    return summary, processed_text

# Create the interface
demo = gr.Interface(
    fn=process_text, # The function to wrap
    inputs=gr.Textbox(lines=5, label="Enter your text here"), # Input
component
    outputs=[ 
        gr.Textbox(label="Text Statistics"),
        gr.Textbox(label="Processed Text")
],
title="Simple Text Processor", # Interface title
description="Enter some text to see word count, character count, and
processing."
)

if __name__ == "__main__":
    demo.launch()