import streamlit as st
import pandas as pd
import os

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

with header:
    st.title("AI in Genetics API")
    st.text("In this project, you can see some Algorithms in AI and Genetics of Biology.")

with dataset:
    st.header("This is my Dataset")
    
    # Load dataset
    df = pd.read_csv("HO_DPR.csv")
    st.write(df.head())

    st.subheader("Get some Value of my Dataset")
    values = pd.DataFrame(df['W_HO_PTA_dpr_SB'].value_counts()).head(20)
    st.bar_chart(values)

with features:
    st.header("The Features I Created:")
    st.markdown('* **This is my first Feature I created because of the check parameters in this dataset.**')

with model_training:
    st.header("Time to Train the Model")
    st.markdown("""
    **Key Observations:**
    - Instead of cyclic encoding, features like month, day, and hour are kept as is.
    - This can simplify the process, but may affect the model's ability to learn cyclic patterns.
    """)
    