from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pickle
import pandas as pd
import numpy as np
import os

app = FastAPI(title="HO_DPR Predictor")

# Load dataset (ensure the file is in the same directory)
if not os.path.exists("HO_DPR.csv"):
    raise FileNotFoundError("Dataset 'HO_DPR.csv' not found.")

df_dpr = pd.read_csv("HO_DPR.csv")

@app.get("/")
def homepage():
    return {"message": "Welcome to the HO_DPR Prediction API"}

class DPRInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: int

@app.post("/predict")
def predict_dpr(payload: DPRInput):
    try:
        # Load the model and scaler
        scaler = pickle.load(open("HOPDR-pipe-nn.pkl", "rb"))
        model = pickle.load(open("HOPDR-pipe-ml.pkl", "rb"))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"File not found: {e}")

    input_data = pd.DataFrame([{
        "feature1": payload.feature1,
        "feature2": payload.feature2,
        "feature3": payload.feature3,
        "feature4": payload.feature4
    }])

    try:
        # Ensure the input data is scaled using the scaler
        input_data_scaled = scaler.transform(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during scaling: {e}")

    try:
        # Predict using the model
        prediction = model.predict(input_data_scaled)
        prediction = np.expm1(prediction)  # Reverse any log transformation, if applicable
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

    return {"prediction": prediction[0]}

if __name__ == "__main__":
    uvicorn.run(app="ho_dpr_api:app", port=8000, host="0.0.0.0", reload=True)