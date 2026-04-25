from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import requests

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("model.pkl")

# AQI API token
TOKEN = "53d7db648757fa8fd99a61898adde391beea2673"

@app.route("/")
def home():
    return "Backend Running ✅"

@app.route("/predict/<city>")
def predict(city):
    try:
        # User inputs
        age = int(request.args.get("age", 30))
        smoking = int(request.args.get("smoking", 0))
        disease = int(request.args.get("disease", 0))

        # AQI API
        url = f"https://api.waqi.info/feed/{city}/?token={TOKEN}"
        response = requests.get(url)
        data = response.json()

        if data["status"] != "ok":
            return jsonify({"error": "City not found ❌"})

        aqi = data["data"]["aqi"]

        # Model prediction
        prediction = model.predict([[aqi, age, smoking]])

        risk_map = {
            0: "Low Risk ✅",
            1: "Medium Risk ⚠️",
            2: "High Risk 🚨"
        }

        disease_map = {
            0: ["No major issues"],
            1: ["Mild Asthma", "Allergies"],
            2: ["Asthma", "Bronchitis", "COPD", "Lung Infection"]
        }

        return jsonify({
            "city": city,
            "aqi": aqi,
            "age": age,
            "smoking": smoking,
            "risk": risk_map[int(prediction[0])],
            "diseases": disease_map[int(prediction[0])]
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()
