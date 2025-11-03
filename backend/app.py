from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import datetime

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Load the trained model and scaler
try:
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
except FileNotFoundError:
    print("Error: model.pkl or scaler.pkl not found.")
    print("Please run the 'car_price_analysis.ipynb' notebook first to generate these files.")
    exit()

# Define the feature order expected by the model
# This MUST match the order from the notebook
# ['Present_Price', 'Kms_Driven', 'Owner', 'Car_Age', 
# 'Fuel_Type_Diesel', 'Fuel_Type_Petrol', 'Seller_Type_Individual', 'Transmission_Manual']
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # --- 1. Extract and Transform Input Data ---
        
        # Numerical features
        present_price = float(data['present_price'])
        kms_driven = int(data['kms_driven'])
        owner = int(data['owner'])
        year = int(data['year'])
        current_year = datetime.datetime.now().year
        car_age = current_year - year
        
        # Categorical features
        fuel_type = data['fuel_type']
        seller_type = data['seller_type']
        transmission = data['transmission']

        # --- 2. Scale Numerical Features ---
        # Create a 2D array for the scaler
        # The scaler expects the features in the SAME order it was trained on:
        # ['Present_Price', 'Kms_Driven', 'Car_Age']
        numerical_features_scaled = scaler.transform([[present_price, kms_driven, car_age]])
        
        scaled_present_price = numerical_features_scaled[0][0]
        scaled_kms_driven = numerical_features_scaled[0][1]
        scaled_car_age = numerical_features_scaled[0][2]

        # --- 3. One-Hot Encode Categorical Features ---
        # These must match the columns from get_dummies(drop_first=True)
        fuel_diesel = 1 if fuel_type == 'Diesel' else 0
        fuel_petrol = 1 if fuel_type == 'Petrol' else 0
        # (If fuel_type is 'CNG', both will be 0, which is correct)

        seller_individual = 1 if seller_type == 'Individual' else 0
        # (If seller_type is 'Dealer', it will be 0, which is correct)
        
        transmission_manual = 1 if transmission == 'Manual' else 0
        # (If transmission is 'Automatic', it will be 0, which is correct)

        # --- 4. Assemble Final Feature Vector ---
        # The order must be IDENTICAL to X_train.columns
        feature_vector = [
            scaled_present_price,
            scaled_kms_driven,
            owner,
            scaled_car_age,
            fuel_diesel,
            fuel_petrol,
            seller_individual,
            transmission_manual
        ]

        # --- 5. Make Prediction ---
        # Reshape to a 2D array (model expects a batch of inputs)
        final_features = [np.array(feature_vector)]
        prediction = model.predict(final_features)

        # Return the prediction as JSON
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the application
if __name__ == '__main__':
    # Host='0.0.0.0' makes it accessible on your network
    app.run(debug=True, host='0.0.0.0')