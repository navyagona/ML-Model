from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Iris Species Predictor API")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'iris_model.joblib')
if os.path.exists(MODEL_PATH):
    model_data = joblib.load(MODEL_PATH)
    model = model_data['model']
    feature_names = model_data['feature_names']
    target_names = model_data['target_names']
else:
    model = None

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
async def root():
    return {"message": "Welcome to the Iris Predictor API"}

@app.post("/predict")
async def predict(data: IrisInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please run train_model.py first.")
    
    # Prepare input for prediction
    input_df = pd.DataFrame([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]], columns=feature_names)
    
    # Get prediction
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    
    species = target_names[prediction]
    confidence = float(probabilities[prediction])
    
    return {
        "species": species,
        "confidence": confidence,
        "probabilities": {name: float(prob) for name, prob in zip(target_names, probabilities)}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
