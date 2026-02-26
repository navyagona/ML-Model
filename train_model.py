import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib
import os

def train_and_save_model():
    print("Loading Iris dataset...")
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training SVM model...")
    model = SVC(probability=True)
    model.fit(X_train, y_train)
    
    # Evaluate (simple)
    score = model.score(X_test, y_test)
    print(f"Model Accuracy: {score:.4f}")
    
    # Save the model and the class names
    model_data = {
        'model': model,
        'feature_names': iris.feature_names,
        'target_names': iris.target_names
    }
    
    model_path = os.path.join(os.path.dirname(__file__), 'iris_model.joblib')
    joblib.dump(model_data, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
