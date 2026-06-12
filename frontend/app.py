import streamlit as st
import os

import pandas as pd
import joblib
from pathlib import Path

st.write("Current Working Directory:")
st.write(os.getcwd())

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(BASE_DIR / "model" / "KNN_heart_model.pkl")
scaler = joblib.load(BASE_DIR / "model" / "heart_scaler.pkl")
expected_columns = joblib.load(BASE_DIR / "model" / "columns.pkl")


st.title("Heart Stroke Prediction By Karan❤️")
st.markdown("Provide the following details")

age = st.slider("Age",18,100,40)
sex = st.selectbox("Sex",['M','F'])
chest_pain = st.selectbox("Chest pain Type",["ATA","NAP","TA","ASY"])
resting_bp = st.number_input("Resting Blood Pressure(mm Hg)", 80,200,120)
cholestrol = st.number_input("Cholestrol(mg/dL)",100,600,200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120mg/dL",[0,1])
resting_ecg = st.selectbox("Resting ECG",["Normal","ST","LVH"])
max_hr = st.slider("Max Heart Rate",60,220,150)
exercise_angina = st.selectbox("Exercise-Induced Angina",["Y","N"])
oldpeak = st.slider("Oldpeak(ST Depression)",0.0,6.0,1.0)
st_slope = st.selectbox("ST Slope",["Up","Flat","Down"])


if st.button("Predict"):

    raw_input = dict.fromkeys(expected_columns,0)

    raw_input.update({
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholestrol,
        "FastingBS": fasting_bs,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,

        "Sex_M": 1 if sex == "M" else 0,

        "ChestPainType_" + chest_pain: 1,
        "RestingECG_" + resting_ecg: 1,
        "ExerciseAngina_" + exercise_angina: 1,
        "ST_Slope_" + st_slope: 1
    })

    input_df = pd.DataFrame([raw_input])

    input_df = input_df.reindex(columns=expected_columns, fill_value=0)

    numeric_cols = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']

    input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.error("⚠️High Risk of Heart Disease")
    else:
        st.success("✅Low Risk of Heart Disease")