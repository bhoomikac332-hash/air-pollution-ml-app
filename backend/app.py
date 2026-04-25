from flask import Flask, jsonify
from flask_cors import CORS
import joblib
import requests

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("model.pkl")

# AQICN API token
TOKEN = "53d7db648757fa8fd99a61898adde391beea2673"

@app.route("/")
def home():
    return "Backend Running ✅"

@app.route("/predict/<city>")
def predict(city):
    try:
        print("City received:", city)

        # AQI API (REAL-TIME DATA)
        url = f"https://api.waqi.info/feed/{city}/?token={TOKEN}"
        response = requests.get(url)
        data = response.json()

        print("API response:", data)

        # Check if city is valid
        if data["status"] != "ok":
            return jsonify({"error": "City not found"})

        # Get AQI value
        aqi = data["data"]["aqi"]

        # Use AQI as input to model
        prediction = model.predict([[aqi, 30, 30]])

        risk_map = {
            0: "Low Risk ✅",
            1: "Medium Risk ⚠️",
            2: "High Risk 🚨"
        }

        return jsonify({
            "city": city,
            "aqi": aqi,
            "risk": risk_map[int(prediction[0])]
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)