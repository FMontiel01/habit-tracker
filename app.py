from flask import Flask, render_template
import json
from datetime import datetime

app = Flask(__name__)


list_of_habits = []
today = datetime.now().date()
try:
    with open("habits.json", "r") as file:
        list_of_habits = json.load(file)
        for habit in list_of_habits:
            counter = 0
            for date in habit['completed_dates']:
                date_object = datetime.strptime(date,"%m/%d/%Y").date()
                delta = today - date_object
                current_week = delta.days
                if 0 <= current_week <= 6:
                    counter += 1
            habit['weekly_progress'] = counter
            if habit['weekly_progress'] > habit['target_days']:
                cap = habit['target_days']
                display_checkmarks = cap
            else:
                display_checkmarks = habit['weekly_progress']
            blank = habit['target_days'] - display_checkmarks

except FileNotFoundError:
    print("Error: 'habits.json' not found.")
except json.JSONDecodeError:
    print("Error: Could not decode JSON from 'habits.json'.")






@app.route("/")
def index():
    return render_template("index.html", my_habits=list_of_habits)

if __name__ == "__main__":
    app.run(debug=True)

