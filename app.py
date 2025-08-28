# app.py
from fastapi import FastAPI
import joblib   # or torch / keras / tensorflow depending on your model
import numpy as np

app = FastAPI()

# Load your trained model (adjust path & library as per your case)
model = joblib.load("models/brain_tumor_model.pkl")

@app.get("/")
def home():
    return {"message": "Brain Tumor Detection API is running 🚀"}

@app.post("/predict")
def predict(data: list):
    # Example: input should be list of features
    features = np.array(data).reshape(1, -1)
    prediction = model.predict(features)[0]
    return {"prediction": int(prediction)}
