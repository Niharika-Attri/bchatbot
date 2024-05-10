from flask import Flask, request, jsonify
import google.generativeai as genai
import pickle
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

google_api_key = os.getenv('google_api_key')
genai.configure(api_key=google_api_key)

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
    
@app.route('/chatbot', methods = ['POST'])
def getResponse():
    if request.method == 'POST':
        user_input = request.get_json(force=True)
        input = user_input.get("input", "not found")
        if( input == "not found"):
            return {"response":"please enter input"}
        else:
            response = get_gemini_response(user_input['input']+"answer the question within 100 words")
            return {"response": response}

if __name__ == '__main__':
    app.run(debug=True)