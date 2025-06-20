import streamlit as st
import pickle
import numpy as np

# Load your trained model
model = pickle.load(open('payments.pkl', 'rb'))

# Page title
st.title("💸 Online Payment Fraud Detection")

# User input fields
st.header("Enter Transaction Details")

step = st.number_input("Step", min_value=1, max_value=1000)
type_code = st.selectbox("Transaction Type", {
    0: "CASH_IN",
    1: "CASH_OUT",
    2: "DEBIT",
    3: "PAYMENT",
    4: "TRANSFER"
})
amount = st.number_input("Amount")
oldbalanceOrg = st.number_input("Old Balance (Origin)")
newbalanceOrig = st.number_input("New Balance (Origin)")
oldbalanceDest = st.number_input("Old Balance (Destination)")
newbalanceDest = st.number_input("New Balance (Destination)")

# Convert type string to code (assuming you trained with encoded values)
type_mapping = {
    "CASH_IN": 0,
    "CASH_OUT": 1,
    "DEBIT": 2,
    "PAYMENT": 3,
    "TRANSFER": 4
}
type_code = type_mapping[type_code]

# Predict button
if st.button("🔍 Predict Fraud"):
    features = np.array([[step, type_code, amount, oldbalanceOrg,
                          newbalanceOrig, oldbalanceDest, newbalanceDest]])
    prediction = model.predict(features)[0]

    if prediction == 1:
        st.error("🚨 Fraudulent Transaction Detected!")
    else:
        st.success("✅ Legitimate Transaction")
