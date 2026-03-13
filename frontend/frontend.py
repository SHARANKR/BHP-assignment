import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("BHP")

st.markdown("Enter the details here:")

sqft = st.number_input("sqft")
bhk = st.number_input("bhk")
bath_room = st.number_input("bath_room")
area = st.selectbox("area", options="1st Block Jayanagar")

if st.button("Price Prediction"):
    input_data = {
        "sqft" : sqft,
        "bhk" : bhk,
        "bath_room" : bath_room,
        "area" : area
    }
    
    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(result)
        else:
            st.error(f"API error : {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect")