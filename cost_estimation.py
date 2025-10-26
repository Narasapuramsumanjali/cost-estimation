# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:31:23 2024

@author: balak
"""

import streamlit as st
import pickle
import numpy as np

# Load the model
model = pickle.load(open("ConstructionCostEstimator.pkl", 'rb'))

# Mapping dictionaries
location_map = {'rural': 0, 'urban': 1, 'suburban': 2, 'metropolitan': 3}
quality_map = {'low': 0, 'medium': 1, 'high': 2}
furnished_map = {'Non-Furnished': 0, 'Furnished': 1}
luxury_map = {'basic': 0, 'standard': 1, 'luxury': 2}
type_map = {'commercial': 0, 'residential': 1}

 
st.title("🏗️ Construction Cost Estimator")
st.subheader("🔥Enter the details of your construction project")

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

    prediction = model.predict(features)
    
    prediction_in_dollars = prediction[0] / 80  # Replace 80 with the current exchange rate if needed
    predicted_price = f"${prediction_in_dollars:,.2f}"
    st.markdown(
    f"<p style='color:black; font-weight:bold; font-size:16px;'>The estimated construction cost is: {predicted_price}</p>", 
    unsafe_allow_html=True)





