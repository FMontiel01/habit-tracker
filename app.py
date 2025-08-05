from flask import Flask, render_template
import json

app = Flask(__name__)

list_of_habits = []
try:
    with open("habits.json", "r") as file:
        list_of_habits = json.load(file)

except FileNotFoundError:
    print("Error: 'habits.json' not found.")
except json.JSONDecodeError:
    print("Error: Could not decode JSON from 'habits.json'.")




@app.route("/")
def index():
    return render_template("index.html", my_habits=list_of_habits)

if __name__ == "__main__":
    app.run(debug=True)

