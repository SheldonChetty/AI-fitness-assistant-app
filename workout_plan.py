from flask import Flask, render_template, request
import random

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
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

if __name__ == "__main__":
    app.run(debug=True)
