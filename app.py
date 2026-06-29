from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

model = pickle.load(open("model/stress_model.pkl", "rb"))
scaler = pickle.load(open("model/scaler.pkl", "rb"))

STRESS_MAP = {
    1: "Very Low",
    2: "Low",
    3: "Moderate",
    4: "High",
    5: "Very High"
}

VALID_RANGE = range(1, 6)  # Features are rated 1–5


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        inputs = [
            int(request.form["sleep_quality"]),
            int(request.form["headache_frequency"]),
            int(request.form["academic_performance"]),
            int(request.form["study_load"]),
            int(request.form["extracurricular_activity"])
        ]

        # Validate input range
        for val in inputs:
            if val not in VALID_RANGE:
                raise ValueError(f"Input value {val} is out of range (1–5).")

        scaled = scaler.transform([inputs])
        prediction = model.predict(scaled)[0]
        stress_label = STRESS_MAP.get(prediction, "Unknown")

        return render_template(
            "index.html",
            prediction=prediction,
            stress_label=stress_label
        )

    except (ValueError, KeyError) as e:
        return render_template(
            "index.html",
            error=f"Invalid input: {str(e)}. Please enter values between 1 and 5."
        )
    except Exception as e:
        return render_template(
            "index.html",
            error="Something went wrong. Please try again."
        )


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)
