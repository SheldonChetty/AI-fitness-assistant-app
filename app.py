from flask import Flask, render_template, request, jsonify
import random
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for


app = Flask(__name__)

# ----------------------------- Chatbot Config -----------------------------
BASE_PROMPT = """
You are Donnie, a friendly gym assistant that helps users build workout routines, answer fitness questions, 
and give suggestions based on fitness goals. Keep responses short, friendly, and only fitness-related.
"""
messages = [{"role": "system", "content": BASE_PROMPT}]
OPENROUTER_API_KEY = "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"

# ----------------------------- Routes -----------------------------


@app.route("/")
def home():
    return render_template("index.html")

# If you want a separate route for 'features.html', change it to something else
# @app.route("/features")
# def features():
#     return render_template("features.html")

@app.route('/features')
def features():
    return render_template("features.html")

@app.route("/tracker")
def tracker():
    num_dishes = 5  # or however many dishes you're expecting
    return render_template("tracker.html", num_dishes=num_dishes)





# @app.route('/nutrition')
# def nutrition():
#     return render_template("tracker.html")

# @app.route('/signin', methods=['GET', 'POST'])
# def signin():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         print("Email entered:", email)
#         print("Password entered:", password)

#         if email == "user@example.com" and password == "password":
#             return redirect(url_for('features'))  # Make sure this function exists
#         else:
#             return render_template('signin.html', error="Invalid credentials. Please try again.")
    
#     return render_template('signin.html')



@app.route('/train')
def train():
    return render_template('train.html')



@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.json["message"]
        messages.append({"role": "user", "content": user_message})

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": messages,
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": reply})
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": f"Error {response.status_code}: {response.text}"}), 500

    return render_template("chatbot.html")





# ----------------------------- Diet Plan Generator -----------------------------

def generate_diet_plan(goal, preference, allergies, days):
    meals_db = {
        "Veg": {
            "Breakfast": ["Poha", "Upma", "Vegetable Dalia", "Idli Sambhar"],
            "Lunch": ["Rajma Rice", "Palak Paneer + Roti", "Chole + Brown Rice"],
            "High Tea": ["Fruit Bowl", "Sprouts Chaat", "Buttermilk", "Roasted Makhana"],
            "Dinner": ["Khichdi", "Veg Pulao", "Mixed Vegetable Curry + Roti"]
        },
        "Non-Veg": {
            "Breakfast": ["Boiled Eggs + Toast", "Chicken Sandwich", "Paneer Bhurji + Toast"],
            "Lunch": ["Grilled Chicken + Rice", "Fish Curry + Roti", "Egg Curry + Brown Rice"],
            "High Tea": ["Boiled Egg Chaat", "Fruit Yogurt", "Peanut Butter Toast"],
            "Dinner": ["Chicken Stew", "Tandoori Fish + Veggies", "Chicken Curry + Roti"]
        }
    }

    selected = "Veg" if preference == "Veg" else "Non-Veg" if preference == "Non-Veg" else random.choice(["Veg", "Non-Veg"])
    if preference == "Vegan":
        selected = "Veg"

    daily_plan = []
    for day in range(1, int(days) + 1):
        b = random.choice(meals_db[selected]["Breakfast"])
        l = random.choice(meals_db[selected]["Lunch"])
        t = random.choice(meals_db[selected]["High Tea"])
        d = random.choice(meals_db[selected]["Dinner"])
        if any(allergy.strip().lower() in f"{b} {l} {t} {d}".lower() for allergy in allergies):
            continue
        calories = random.randint(1500, 2200)
        daily_plan.append({
            "day": day,
            "breakfast": b,
            "lunch": l,
            "tea": t,
            "dinner": d,
            "calories": calories
        })

    return daily_plan

@app.route("/diet_form", methods=["GET", "POST"])
def diet_form():
    if request.method == "POST":
        goal = request.form["goal"]
        preference = request.form["preference"]
        allergies = request.form["allergies"].split(",")
        days = int(request.form["days"])

        diet_plan = generate_diet_plan(goal, preference, allergies, days)
        return render_template("diet_result.html", diet_plan=diet_plan)

    return render_template("diet_form.html")


# ----------------------------- Workout Plan Generator -----------------------------

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)

def generate_workout_plan(gender, age, height, weight, days, workout_type, equipment, goal, health_issue):
    workouts_db = {
        "Home Workout": ["Jumping Jacks", "Push-ups", "Squats", "Lunges", "Mountain Climbers", "Plank", "High Knees"],
        "Gym Workout": ["Bench Press", "Deadlift", "Leg Press", "Lat Pulldown", "Cable Rows", "Shoulder Press", "Barbell Squat"],
        "Yoga": ["Sun Salutation", "Tree Pose", "Bridge Pose", "Cobra Stretch", "Warrior Pose", "Child’s Pose"]
    }

    plan = []
    for day in range(1, int(days) + 1):
        daily = []
        for ex in random.sample(workouts_db[workout_type], k=4):
            sets = random.randint(3, 5)
            reps = random.choice([10, 12, 15])
            daily.append(f"{ex} ({sets} sets x {reps} reps)")
        plan.append((f"Day {day}", daily))

    return calculate_bmi(height, weight), plan

@app.route("/workout_form", methods=["GET", "POST"])
def workout_form():
    if request.method == "POST":
        gender = request.form["gender"]
        age = int(request.form["age"])
        height = int(request.form["height"])
        weight = int(request.form["weight"])
        days = int(request.form["days"])
        workout_type = request.form["workout_type"]
        equipment = request.form["equipment"]
        goal = request.form["goal"]
        health = request.form["health"]

        bmi, plan = generate_workout_plan(gender, age, height, weight, days, workout_type, equipment, goal, health)
        return render_template("workout_result.html", bmi=bmi, plan=plan)

    return render_template("workout_form.html")


# ----------------------------- Run App -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
