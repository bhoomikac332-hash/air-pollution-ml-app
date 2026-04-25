from flask import Flask, jsonify
from flask_cors import CORS
import joblib
import requests

app = Flask(__name__)
CORS(app)

model = joblib.load("model.pkl")

API_KEY = "YOUR_API_KEY_HERE"

@app.route("/")
def home():
    return "Server Running"

@app.route("/predict_location/<lat>/<lon>")
def predict_location(lat, lon):
    try:
        TOKEN = "YOUR_AQICN_TOKEN"

        url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={TOKEN}"
        data = requests.get(url).json()

        if data["status"] != "ok":
            return jsonify({"error": "Location not found"})

        aqi = data["data"]["aqi"]

        prediction = model.predict([[aqi, 30, 30]])

        risk_map = {
            0: "Low Risk ✅",
            1: "Medium Risk ⚠️",
            2: "High Risk 🚨"
        }

        return jsonify({
            "city": data["data"]["city"]["name"],
            "aqi": aqi,
            "risk": risk_map[int(prediction[0])]
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    