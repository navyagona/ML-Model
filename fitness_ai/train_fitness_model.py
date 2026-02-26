import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

def generate_and_train():
    print("Generating synthetic fitness dataset...")
    # Features: Duration (min), HeartRate (bpm), BMI, Age
    np.random.seed(42)
    n_samples = 1000
    
    duration = np.random.uniform(10, 120, n_samples)
    heart_rate = np.random.uniform(100, 180, n_samples)
    bmi = np.random.uniform(18, 35, n_samples)
    age = np.random.uniform(18, 70, n_samples)
    
    # Simple formula for calories: duration * heart_rate * factor + bmi_offset - age_offset
    # This is just for demonstration, not medically accurate.
    calories = (duration * 0.05) * (heart_rate * 0.07) + (bmi * 2) - (age * 0.5) + np.random.normal(0, 10, n_samples)
    
    X = pd.DataFrame({
        'duration': duration,
        'heart_rate': heart_rate,
        'bmi': bmi,
        'age': age
    })
    y = calories
    
    print("Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X, y)
    
    print(f"Model R^2 score: {model.score(X, y):.4f}")
    
    model_path = os.path.join(os.path.dirname(__file__), 'fitness_model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    generate_and_train()
