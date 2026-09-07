import os
import sys
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add root directory to sys.path so linear_regression module can be imported
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from linear_regression import LinearRegression

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# Locate dataset
csv_candidates = [
    os.path.join(BASE_DIR, "simple_linear_regression.csv"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_linear_regression.csv"),
    os.path.join(os.getcwd(), "simple_linear_regression.csv"),
    "simple_linear_regression.csv"
]

csv_path = None
for candidate in csv_candidates:
    if os.path.exists(candidate):
        csv_path = candidate
        break

# Train Linear Regression Model on cold start
x = []
y = []

if csv_path and os.path.exists(csv_path):
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 2 and row[0].strip() and row[1].strip():
                try:
                    x.append(float(row[0]))
                    y.append(float(row[1]))
                except ValueError:
                    continue

if x and y:
    model = LinearRegression(x=x, y=y, alpha=0.001)
    model.fit()
else:
    model = None


@app.route("/", methods=["GET"])
def home():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return app.send_static_file("index.html")
    return jsonify({"message": "Salary Predictor API is running."})


@app.route("/api/predict", methods=["GET", "POST", "OPTIONS"])
@app.route("/predict", methods=["GET", "POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return "", 204

    experience = None

    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        if data:
            for key in ["experience", "years", "years_experience", "YearsExperience"]:
                if key in data and data[key] is not None:
                    experience = data[key]
                    break

    if experience is None:
        for key in ["experience", "years", "years_experience", "YearsExperience"]:
            if key in request.args:
                experience = request.args.get(key)
                break

    if experience is None:
        return jsonify({
            "success": False,
            "error": "Missing 'experience' parameter. Provide JSON {'experience': 3.5} or query param ?experience=3.5"
        }), 400

    try:
        exp_float = float(experience)
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Invalid value for 'experience'. Must be a number."
        }), 400

    if exp_float < 0:
        return jsonify({
            "success": False,
            "error": "Experience cannot be negative."
        }), 400

    if model is None:
        return jsonify({
            "success": False,
            "error": "Model failed to initialize or dataset could not be loaded."
        }), 500

    predicted_salary = model.predict(exp_float)

    return jsonify({
        "success": True,
        "experience": exp_float,
        "salary": round(predicted_salary, 2),
        "predicted_salary": round(predicted_salary, 2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
