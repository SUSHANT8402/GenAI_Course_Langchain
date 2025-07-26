import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle
import logging
import os
from datetime import datetime

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f"churn_app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define base directory (where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define file paths relative to script location
MODEL_PATH = os.path.join(BASE_DIR, "model.h5")
GENDER_ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder_gender.pkl")
GEO_ENCODER_PATH = os.path.join(BASE_DIR, "onehot_encoder_geo.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

# Load model and encoders/scalers
try:
    model = tf.keras.models.load_model(MODEL_PATH)

    with open(GENDER_ENCODER_PATH, 'rb') as file:
        label_encoder_gender = pickle.load(file)

    with open(GEO_ENCODER_PATH, 'rb') as file:
        onehot_encoder_geo = pickle.load(file)

    with open(SCALER_PATH, 'rb') as file:
        scaler = pickle.load(file)

except Exception as e:
    st.error("Failed to load model or preprocessing components.")
    logging.exception("Error during model/loading phase.")
    st.stop()

# Streamlit UI
st.title('Customer Churn Prediction')

try:
    geography = st.selectbox('Geography*', onehot_encoder_geo.categories_[0])
    gender = st.selectbox('Gender*', label_encoder_gender.classes_)
    age = st.slider('Age*', 18, 90)
    credit_score = st.number_input('Credit Score*', min_value=300, max_value=900, value=600)
    balance = st.number_input('Balance*', min_value=0.0)
    estimated_salary = st.number_input('Estimated Salary*', min_value=0.0)
    tenure = st.slider('Tenure*', 0, 10)
    num_of_products = st.slider('Number of Products*', 1, 4)
    has_cr_card = st.selectbox('Has Credit Card*', [0, 1])
    is_active_member = st.selectbox('Is Active Member*', [0, 1])

    if st.button("Predict"):
        try:
            # Input validation (extra)
            if any(val is None for val in [geography, gender, age, credit_score, balance, estimated_salary, tenure, num_of_products]):
                st.warning("All fields marked with * are required.")
                st.stop()

            # Log input
            logging.info(f"Inputs - Geo: {geography}, Gender: {gender}, Age: {age}, Credit: {credit_score}, "
                         f"Balance: {balance}, Salary: {estimated_salary}, Tenure: {tenure}, "
                         f"Products: {num_of_products}, Card: {has_cr_card}, Active: {is_active_member}")

            # Encode inputs
            gender_encoded = label_encoder_gender.transform([gender])  # shape: (1,)
            geography_encoded = onehot_encoder_geo.transform([[geography]]).toarray()  # shape: (1, 3)
            numerical_features = np.array([[credit_score, age, tenure, balance, num_of_products, has_cr_card, is_active_member, estimated_salary]])  # shape: (1, 8)

            # Combine
            all_features = np.concatenate([geography_encoded, gender_encoded.reshape(-1, 1), numerical_features], axis=1)
            features_scaled = scaler.transform(all_features)

            # Predict
            prediction = model.predict(features_scaled)
            churn_prob = prediction[0][0]

            # Log result
            logging.info(f"Churn Probability: {churn_prob:.4f}")

            # Display probability value
            st.metric(label="Churn Probability", value=f"{churn_prob * 100:.2f}%")

            # Display result message
            if churn_prob > 0.5:
                st.error("Customer is likely to churn.")
            else:
                st.success("Customer is likely to stay.")

        except Exception as e:
            st.error("Prediction failed due to an internal error. Please check inputs and try again.")
            logging.exception("Error during prediction phase.")

except Exception as e:
    st.error("App failed to render properly.")
    logging.exception("Error in main Streamlit layout.")
