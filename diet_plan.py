from flask import Flask, render_template, request
import random

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        goal = request.form["goal"]
        preference = request.form["preference"]
        allergies = request.form["allergies"].split(",")
        days = int(request.form["days"])

        diet_plan = generate_diet_plan(goal, preference, allergies, days)
        return render_template("diet_result.html", diet_plan=diet_plan)

    return render_template("diet_form.html")

if __name__ == "__main__":
    app.run(debug=True)
