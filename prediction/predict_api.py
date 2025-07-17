from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model = joblib.load("salinity_model.pkl") 

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    input_values = [data.get(k, 0) for k in ["depsm", "tv290c", "conductivity_s_per_m", "secchi_depth_m", 
                                             "ph", "dissolved_oxygen_pct", "dissolved_oxygen_mgl"]]
    prediction = model.predict([input_values])[0]
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)

