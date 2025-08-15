from flask import Flask, render_template, redirect, url_for, request
import json
from datetime import datetime
import uuid

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
                display_checkmarks = habit['target_days']
            else:
                display_checkmarks = habit['weekly_progress']
            blanks = habit['target_days'] - display_checkmarks
            habit['emoji_bar'] = "✅" * display_checkmarks + "⬜" * blanks

except FileNotFoundError:
    print("Error: 'habits.json' not found.")
except json.JSONDecodeError:
    print("Error: Could not decode JSON from 'habits.json'.")


@app.route("/")
def index():
    return render_template("index.html", my_habits=list_of_habits)

@app.route('/complete', methods=['POST'])
def complete():
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    #Read and normalize inputs
    name = (request.form.get('name') or '').strip()
    category_select = (request.form.get('category') or '').strip()
    category_custom = (request.form.get('category_custom') or '').strip()
    target_raw = (request.form.get('target_days') or '').strip()

    # Choose final category (custom overides select)
    category = category_custom if category_custom else category_select
    category = category.strip().title() if category else 'Other'

    #Validate inputs
    if not (1 <= len(name) <= 40):
        return redirect(url_for('index'))
    if any(habit['name'].lower() == name.lower() for habit in list_of_habits):
        return redirect(url_for('index'))

    # Target days: integer in [1-7]
    try:
        target_days = int(target_raw)
    except ValueError:
        return redirect(url_for('index'))
    if not (1 <= target_days <= 7):
        return redirect(url_for('index'))

    #Category: 2-24 chars (fallback to 'Other' if too short)
    if len(category) < 2 or len(category) > 24:
        category = 'Other'

    # Build the habit object
    habit = {
        'id': str(uuid.uuid4()),
        'name': name,
        'category': category,
        'target_days': target_days,
        'date_created': date.today().isoformat(),
        'completed_dates': [],
        'weekly_progress': 0,
        'emoji_bar': ''
    }

    #Save + PRG redirect
    list_of_habits.append(habit)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
