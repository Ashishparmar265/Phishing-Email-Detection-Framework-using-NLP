import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.preprocessing.data_pipeline import DataPreprocessor
from src.extraction.feature_extractor import FeatureExtractor

app = FastAPI(title="Phishing Email Detection API")

# Load models and transformers
try:
    model = joblib.load("models/rf_model.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    vectorizer = None

preprocessor = DataPreprocessor()
extractor = FeatureExtractor()

class EmailInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Phishing Email Detection API is running"}

@app.post("/predict")
def predict(email: EmailInput):
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    # 1. Feature Extraction & Masking
    feats, masked_text = extractor.extract_all(email.text)
    
    # 2. Preprocessing
    clean_text = preprocessor.full_pipeline(masked_text)
    
    # 3. Vectorization
    tfidf_feat = vectorizer.transform([clean_text]).toarray()
    
    # 4. Combine Features
    custom_feat = np.array(list(feats.values())).reshape(1, -1)
    X = np.hstack((tfidf_feat, custom_feat))
    
    # 5. Prediction
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]
    
    return {
        "prediction": "Phishing" if prediction == 1 else "Ham",
        "phishing_probability": float(probability),
        "extracted_features": feats
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
