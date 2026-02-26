from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Fitness AI - Calories Burned Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'fitness_model.joblib')
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

class FitnessInput(BaseModel):
    duration: float
    heart_rate: float
    bmi: float
    age: float

@app.get("/")
async def root():
    return {"message": "Fitness AI API is running"}

@app.post("/predict")
async def predict(data: FitnessInput):
    if model is None:
        return {"error": "Model not found. Run train_fitness_model.py first."}
    
    input_df = pd.DataFrame([[
        data.duration,
        data.heart_rate,
        data.bmi,
        data.age
    ]], columns=['duration', 'heart_rate', 'bmi', 'age'])
    
    prediction = model.predict(input_df)[0]
    return {"calories_burned": round(float(prediction), 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
