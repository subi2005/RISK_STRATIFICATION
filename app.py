from fastapi import FastAPI
import joblib

app = FastAPI()

# Load model
model = joblib.load("model.pkl")

@app.get("/")
def root():
    return {"message": "Model API is running on Azure!"}

@app.post("/predict")
def predict(features: dict):
    data = list(features.values())
    prediction = model.predict([data])
    return {"prediction": prediction.tolist()}
