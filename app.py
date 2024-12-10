from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pickle
import pandas as pd
import numpy as np

app = FastAPI(title="HO_DPR Predictor")

# Load dataset (ensure the file is in the same directory)
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
    scaler = pickle.load(open("ho_dpr_scaler.pkl", "rb"))
    model = pickle.load(open("ho_dpr_model.pkl", "rb"))

    input_data = pd.DataFrame([{
        "feature1": payload.feature1,
        "feature2": payload.feature2,
        "feature3": payload.feature3,
        "feature4": payload.feature4
    }])

    input_data_scaled = scaler.transform(input_data)

    prediction = model.predict(input_data_scaled)
    prediction = np.expm1(prediction)

    return {"prediction": prediction[0]}

if __name__ == "__main__":
    uvicorn.run(app="ho_dpr_api:app",
                port=8000,
                host="0.0.0.0",
                reload=True)
