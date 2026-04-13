from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv #will allow you to pull api key from secure place
###from google import genai #not working for now.
import google.generativeai as genai

app = Flask(__name__)
load_dotenv() # loads .env file
api_key = os.getenv("GEMINI_API_KEY") #get api key
client = genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


@app.route('/', methods=['POST', 'GET']) #now the website can sent and recive 
def index():
    response_text = ""
    flashcards = []  # Move here so it always exists

    if request.method == "POST":
        user_text = request.form["user_input"]

        prompt = f"""
        Turn the following text into flashcards.

        Format:
        Question: ...
        Answer: ...

        Text:
        {user_text}
        """

        response = model.generate_content(prompt)
        output_text = response.text  # Define BEFORE using it
        response_text = output_text

        cards = output_text.split("Question:")

        for card in cards:
            if "Answer:" in card:
                question, answer = card.split("Answer:")
                flashcards.append({
                    "question": question.strip(),
                    "answer": answer.strip()
                })

    return render_template(
        "index.html",
        flashcards=flashcards
    )


if __name__ == '__main__':
    app.run(debug=True)




    #you need to activate environment?? for what reason?
    #to activate --> .\env\Scripts\Activate.ps1
    #also you need to deactivate with --> deactivate

