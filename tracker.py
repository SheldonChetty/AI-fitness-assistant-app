from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.graph_objs as go

app = Flask(_name_)

# Load CSV safely
CSV_PATH = "food.csv"
try:
    df = pd.read_csv(CSV_PATH)
except Exception as e:
    df = pd.DataFrame(columns=["Food", "Calories"])
    print("Error loading CSV:", e)

@app.route("/", methods=["GET", "POST"])
def tracker():
    food_items = df["Food"].tolist()
    num_dishes = 1
    food_inputs = []
    total = 0
    chartJSON = None

    if request.method == "POST":
        num_dishes = int(request.form.get("num_dishes", 1))
        calories_data = []

        for i in range(num_dishes):
            food = request.form.get(f"food_{i}", food_items[0])
            servings = int(request.form.get(f"serving_{i}", 1))

            cal = df[df["Food"] == food]["Calories"].values[0]
            total_cal = cal * servings
            food_inputs.append({"food": food, "servings": servings, "calories": total_cal})
            calories_data.append((food, total_cal))

        total = sum([item[1] for item in calories_data])

        # Chart
        chart = go.Figure(data=[go.Pie(labels=[f for f, _ in calories_data],
                                       values=[c for _, c in calories_data],
                                       textinfo='label+percent')],
                          layout=go.Layout(title="Calories by Food"))
        chartJSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("tracker.html",
                           food_items=food_items,
                           num_dishes=num_dishes,
                           food_inputs=food_inputs,
                           total=total,
                           chartJSON=chartJSON)

if _name_ == "_main_":
    app.run(debug=True)