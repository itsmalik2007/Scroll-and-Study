from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv #will allow you to pull api key from secure place
import google.generativeai as genai
import json



#Load flashcards at startup
FLASHCARD_FILE = "flashcards.json"

def load_flashcards():
    if os.path.exists(FLASHCARD_FILE):
        with open(FLASHCARD_FILE, "r") as f:
            return json.load(f)

    return []



def save_flashcards(cards):
    with open(FLASHCARD_FILE, "w") as f:
        json.dump(cards, f, indent=4)



app = Flask(__name__)
load_dotenv() # loads .env file
api_key = os.getenv("GEMINI_API_KEY") #get api key
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


@app.route('/', methods=['POST', 'GET']) #now the website can sent and recive 
def index():
    response_text = ""
    flashcards = load_flashcards()


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

        output_text = response.text 
                
        cards = output_text.split("Question:")

        for card in cards:

            if "Answer:" in card:

                parts = card.split("Answer:")

                if len(parts) == 2:

                    question = parts[0].strip()
                    answer = parts[1].strip()

                    if question and answer:

                        new_id = len(flashcards) + 1

                        new_card = {
                            "id": new_id,
                            "question": question,
                            "answer": answer
                        }

                        # Prevent duplicates
                        if new_card not in flashcards:
                            flashcards.append(new_card)

        save_flashcards(flashcards)

        return redirect(url_for("index"))


    return render_template(
        "index.html",
        flashcards=flashcards
    )



#Adds delete function for flashcards
@app.route("/delete/<int:card_id>")
def delete(card_id):

    flashcards = load_flashcards()

    flashcards = [
        card for card in flashcards
        if card["id"] != card_id
    ]

    save_flashcards(flashcards)

    return redirect(url_for("index"))
    


#Adds edit function for flashcards
@app.route("/edit/<int:card_id>", methods=["GET", "POST"])
def edit(card_id):

    flashcards = load_flashcards()

    card_to_edit = None

    for card in flashcards:

        if card["id"] == card_id:
            card_to_edit = card
            break

    if request.method == "POST":

        card_to_edit["question"] = request.form["question"]
        card_to_edit["answer"] = request.form["answer"]

        save_flashcards(flashcards)

        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        card=card_to_edit
    )


if __name__ == '__main__':
    app.run(debug=True)




    #you need to activate environment?? for what reason?
    #to activate --> .\env\Scripts\Activate.ps1
    #also you need to deactivate with --> deactivate

