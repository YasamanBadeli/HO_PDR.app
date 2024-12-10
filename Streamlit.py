import streamlit as st
import pandas as pd
import requests
import base64
import time
from urllib.parse import urlencode

# Define mappings for dropdown menus
Size = {0: "Small", 1: "Big"}
Temp = {0: "Low", 1: "Medium", 2: "High"}

def main():
    # Title and description
    st.title(":green[Predicting Livestock Milk Production Based on Various Livestock Characteristics] 🐄")
    st.markdown("""
    Welcome to the Prediction System! 
    This app helps predict livestock milk production and analyze changes in prices over the years.
    """)

    # Model selection
    model_type = st.selectbox("Select your model", ["Neural Network", "Linear Regression"])
    st.write(f"The model **{model_type}** was selected.")

    # Load dataset
    try:
        df = pd.read_csv("HO_DPR.csv")
    except FileNotFoundError:
        st.error("Dataset 'HO_DPR.csv' not found. Please ensure the file is available.")
        return

    # Sidebar inputs
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

        base_url = "https://HODPR-api-url.com/predict?"
        url = base_url + urlencode(params)

        # Display prediction results
        with st.spinner("Classifying, please wait..."):
            time.sleep(2)
            response = requests.get(url)

            if response.status_code == 200:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    try:
                        result = response.json()

                        # Handle image in response if present
                        if "zu1.jpg" in result:
                            img = result["zu1.jpg"]
                            img_decoded = base64.b64decode(img)
                            st.image(img_decoded)
                            st.success("Prediction completed successfully!")
                        else:
                            st.error("The image was not found in the response.")
                    except ValueError as e:
                        st.error(f"Failed to parse response as JSON: {e}")
                        st.error(f"Response content: {response.text}")
                else:
                    st.error("The response content is not in JSON format.")
                    st.error(f"Response content: {response.text}")
            else:
                st.error(f"Request failed with status code: {response.status_code}")
                st.error(f"Response content: {response.text}")
import requests

try:
    response = requests.get("https://hodpr-api-url.com/predict")
    print(response.status_code, response.text)
except requests.ConnectionError as e:
    print(f"Connection error: {e}")
    
if __name__ == "__main__":
    # Style sidebar
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