import pathlib
import textwrap
import google.generativeai as genai
#from google.colab import userdata
from IPython.display import display
from IPython.display import Markdown
import os
from dotenv import load_dotenv
load_dotenv()

import pickle

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, ">", predicate=lambda _: True))

google_api_key = os.getenv('google_api_key')
genai.configure(api_key=google_api_key)

model = genai.GenerativeModel('models/gemini-1.0-pro-latest')

def is_topic_specific(response):
    keywords = ["animal cell", "plant cell","chemical bonds","photosynthesis","covalent bond","solar system","earth","science","motherboard",'mitochondira',
                "cell wall",'cellulose','technology','cell organelles','biology']
    response_text = response.text.lower()
    for keyword in keywords:
        if keyword in response_text:
            return True
    return False

def get_gemini_response(user_input):
    response = model.generate_content(user_input)
    if is_topic_specific(response):
        return response.text
    else:
        return "I'm sorry! Why not talk about the things you just studied right now!"

while True:
    user_input = input("Ask your question (type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    response_text = get_gemini_response(user_input) + "answer the question within 100 words"
    print(response_text)
    #display(to_markdown(response_text))

pickle.dump(model, open('model.pkl', 'wb'))
nmodel = pickle.load(open('model.pkl','rb'))