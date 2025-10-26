# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:31:23 2024

@author: balak
"""

import streamlit as st
import pickle
import numpy as np
from num2words import num2words

# Load the model
model = pickle.load(open("ConstructionCostEstimator.pkl", 'rb'))

# Mapping dictionaries
location_map = {'rural': 0, 'urban': 1, 'suburban': 2, 'metropolitan': 3}
quality_map = {'low': 0, 'medium': 1, 'high': 2}
furnished_map = {'Non-Furnished': 0, 'Furnished': 1}
luxury_map = {'basic': 0, 'standard': 1, 'luxury': 2}
type_map = {'commercial': 0, 'residential': 1}

# Background function
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://wallpapercave.com/wp/wp2662866.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background
add_bg_from_url()

# Title
st.markdown(
    """
    <h1 style='text-align: center; color: #0078D7; 
               text-shadow: 2px 2px 5px rgba(0,0,0,0.3); 
               font-size: 50px; font-weight: bold;'>🏗️ Construction Cost Estimator</h1>
    """,
    unsafe_allow_html=True
)

# Subtitle
st.markdown(
    """
    <h3 style='color: #000000; 
               text-shadow: 1px 1px 2px rgba(255,255,255,0.4); 
               font-size: 26px; font-weight: 600;'>Enter the details of your construction project:</h3>
    """,
    unsafe_allow_html=True
)

# UI Styling
st.markdown("""
    <style>
    label {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }

    .stSelectbox label, .stNumberInput label {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    .stButton>button {
        background-color: #0078D7;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #005a9e;
        color: #ffffff;
    }

    .stApp {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Input fields
location = st.selectbox("Location:", list(location_map.keys()))
type_of_property = st.selectbox("Property Type:", list(type_map.keys()))
floor = st.number_input("Number of Floors:", min_value=0, step=1, format="%d")
sqft = st.number_input("Total Area (in sqft):", min_value=0.0, step=0.1, format="%.2f")
quality = st.selectbox("Construction Quality:", list(quality_map.keys()))
furnished = st.selectbox("Furnished Type:", list(furnished_map.keys()))
luxury = st.selectbox("Luxury Level:", list(luxury_map.keys()))

# Prediction logic
if st.button("Predict Cost"):
    location_encoded = location_map.get(location, -1)
    quality_encoded = quality_map.get(quality, -1)
    furnished_encoded = furnished_map.get(furnished, -1)
    luxury_encoded = luxury_map.get(luxury, -1)
    type_encoded = type_map.get(type_of_property, -1)

    features = np.array(
        [[location_encoded, type_encoded, floor, sqft, quality_encoded, furnished_encoded, luxury_encoded]]
    )

    prediction = model.predict(features)[0]

    # Round prediction to nearest rupee
    prediction = round(prediction)

    # Number formatting
    predicted_price = f"₹{prediction:,.0f}"

    # Convert to words (Indian style)
    price_in_words = num2words(prediction, lang='en_IN').title()
    price_in_words = price_in_words.replace("And", "and")

    # Display result
    st.markdown(
        f"""
        <p style='color:black; font-weight:bold; font-size:18px;'>
            The estimated construction cost is: {predicted_price}
        </p>
        <p style='color:#0078D7; font-weight:600; font-size:16px;'>
            ({price_in_words} Rupees Only)
        </p>
        """,
        unsafe_allow_html=True
    )

