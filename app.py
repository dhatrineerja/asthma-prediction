import streamlit as st
import pandas as pd
import joblib
import os

# Load trained pipeline
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(PROJECT_ROOT, "models", "best_model.pkl")

model = joblib.load(model_path)

# App Title
st.set_page_config(page_title="Asthma Risk Prediction", page_icon="A", layout="centered")
st.title("Asthma Risk Prediction App")
st.markdown("Predict the **risk of asthma** based on patient health, environment, and lifestyle factors.")

st.divider()

# Center Layout
col1, col2, col3 = st.columns([1, 2, 1])  # keep inputs centered

with col2:
    # Button styling only (no card box)
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 24px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

    # Headers
    st.header("Patient Information")

    # Numerical inputs
    age = st.slider("Age", 0, 100, 30)
    bmi = st.slider("BMI", 10.0, 60.0, 22.5, step=0.1)
    family_history = st.radio("Family History of Asthma", [0, 1], horizontal=True,
                              format_func=lambda x: "Yes" if x == 1 else "No")
    med_adherence = st.slider("Medication Adherence (0–10)", 0, 10, 5)
    er_visits = st.slider("Number of ER Visits", 0, 50, 0)
    pef = st.slider("Peak Expiratory Flow", 100, 800, 400)
    feno = st.slider("FeNO Level (ppb)", 5, 200, 25)

    # Categorical inputs
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
    allergies = st.radio("Allergies", ["Yes", "No"], horizontal=True)
    air_pollution = st.selectbox("Air Pollution Level", ["Low", "Medium", "High"])
    physical_activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
    occupation = st.selectbox("Occupation Type", ["Office", "Manual Labor", "Other"])
    comorbidities = st.selectbox("Comorbidities", ["None", "Diabetes", "Hypertension", "Other"])

    # Input DataFrame
    input_data = pd.DataFrame({
        "Age": [age],
        "Gender": [gender],
        "BMI": [bmi],
        "Smoking_Status": [smoking],
        "Family_History": [family_history],
        "Allergies": [allergies],
        "Air_Pollution_Level": [air_pollution],
        "Physical_Activity_Level": [physical_activity],
        "Occupation_Type": [occupation],
        "Comorbidities": [comorbidities],
        "Medication_Adherence": [med_adherence],
        "Number_of_ER_Visits": [er_visits],
        "Peak_Expiratory_Flow": [pef],
        "FeNO_Level": [feno]
    })

    # Prediction button
    if st.button("Predict Asthma Risk", use_container_width=True):
        prediction = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1]

        st.subheader("Prediction Result:")
        if prediction == 1:
            st.error(f"High Risk of Asthma (Probability: {prob:.2%})")
        else:
            st.success(f"Low Risk of Asthma (Probability: {prob:.2%})")

        # Probability bar
        st.progress(int(prob * 100))





