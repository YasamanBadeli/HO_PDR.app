import streamlit as st
import pandas as pd
import requests
import base64
import time
from urllib.parse import urlencode
from fastapi import FastAPI
from pydantic import BaseModel

# Define mappings for dropdown menus

Temp = {0: "Low", 1: "Medium", 2: "High"}
Size = {0: "Small", 1: "Big"}

def load_data():
    try:
        df = pd.read_csv("HO_DPR.csv")
        return df
    except FileNotFoundError:
        st.error("Dataset 'HO_DPR.csv' not found. Please ensure the file is available.")
        return None

def main():
    st.title(":green[Predicting Livestock Milk Production Based on Various Livestock Characteristics] 🐄")
    st.markdown("""
    Welcome to the Prediction System! 
    This app helps predict livestock milk production and analyze changes in prices over the years.
    """)

    model_type = st.selectbox("Select your model", ["Neural Network", "Linear Regression"])
    st.write(f"The model **{model_type}** was selected.")

    df = load_data()
    if df is None:
        return

    with st.sidebar:
        st.header(":pink[Insert Your Data for Prediction]")

        HO_ptadpr_AllCow_3 = st.slider(
            "HO_ptadpr_AllCow_3",
            min_value=int(df['HO_ptadpr_AllCow_3'].min()),
            max_value=int(df['HO_ptadpr_AllCow_3'].max()),
            value=int(df['HO_ptadpr_AllCow_3'].mean()),
            step=1
        )

        yob7 = st.selectbox("yob7", options=Temp.keys(), format_func=lambda x: Temp[x])

        UW_BY1_HO_PTA_dpr_SB = st.slider(
            "UW_BY1_HO_PTA_dpr_SB",
            min_value=float(df['UW_BY1_HO_PTA_dpr_SB'].min()),
            max_value=float(df['UW_BY1_HO_PTA_dpr_SB'].max()),
            value=float(df['UW_BY1_HO_PTA_dpr_SB'].mean()),
            step=0.5
        )

        HO_ptadpr_RegCow_7 = st.selectbox(
            "HO_ptadpr_RegCow_7",
            options=Size.keys(),
            format_func=lambda x: Size[x]
        )

        HO_numdpr_RegCow = st.slider(
            "HO_numdpr_RegCow",
            min_value=0.0,
            max_value=5.0,
            value=float(df['HO_numdpr_RegCow'].mean()),
            step=0.1
        )

        HO_numdpr_AllCow = st.checkbox("HO_numdpr_AllCow")
        classify = st.button("**Click**")

        # Prepare API request parameters
        params = {
            "HO_ptadpr_AllCow_3": HO_ptadpr_AllCow_3,
            "yob7": yob7,
            "UW_BY1_HO_PTA_dpr_SB": UW_BY1_HO_PTA_dpr_SB,
            "HO_ptadpr_RegCow_7": HO_ptadpr_RegCow_7,
            "HO_numdpr_RegCow": HO_numdpr_RegCow,
            "HO_numdpr_AllCow": int(HO_numdpr_AllCow),
            "model_type": model_type
        }

        base_url = "http://127.0.0.1:8000/predict"

        if classify:
            with st.spinner("Classifying, please wait..."):
                time.sleep(2)

            response = requests.post(base_url, json=params)
            if response.status_code == 200:
                result = response.json()

                img = result.get("Benefices-Dry-Cow-800.png")
                if img:
                    img_decoded = base64.b64decode(img)
                    st.image(img_decoded)
                else:
                    st.error("No image returned from the server.")
            else:
                st.error("An error occurred")
                st.error(response.json())

app = FastAPI()

class InputData(BaseModel):
    HO_ptadpr_AllCow_3: int
    yob7: int
    UW_BY1_HO_PTA_dpr_SB: float
    HO_ptadpr_RegCow_7: int
    HO_numdpr_RegCow: float
    HO_numdpr_AllCow: int
    model_type: str

@app.post("/predict")
def predict(data: InputData):
    return {"message": "Data received successfully"}

    st.write(df)

    st.header("Prediction")
    pipe = pickle.load(open("titanic-pipe.pkl", "rb"))
    prediction = pipe.predict(df)
    if prediction[0] == 0:
        st.subheader("💀 **DEAD**")
        st.snow()
    else:
        st.subheader("👍 **ALIVE**")
        st.balloons()
        
if __name__ == "__main__":
    st.sidebar.markdown(
        """
        <style>
            [data-testid=stSidebar] {
                background-color: #f6c7db;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    main()