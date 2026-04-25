import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.preprocessing.data_pipeline import DataPreprocessor
from src.extraction.feature_extractor import FeatureExtractor
from src.classification.lstm_model import PhishingLSTM
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Phishing Email Detection API")

# Add CORS Middleware to allow frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load models and transformers
try:
    # 1. Load Baseline (Random Forest)
    rf_model = joblib.load("models/rf_model.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")
    
    # 2. Load Advanced (Bi-LSTM)
    lstm_engine = PhishingLSTM()
    lstm_engine.model = tf.keras.models.load_model("models/phishing_lstm.h5")
    with open("models/phishing_lstm_tokenizer.pkl", "rb") as f:
        lstm_engine.tokenizer = joblib.load(f)
        
    print("SUCCESS: All models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    rf_model = None
    vectorizer = None
    lstm_engine = None

preprocessor = DataPreprocessor()
extractor = FeatureExtractor()

class EmailInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Phishing Email Detection API is running", "models_loaded": lstm_engine is not None}

@app.post("/predict")
def predict(email: EmailInput):
    if not rf_model or not lstm_engine:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    # --- Step 1: Feature Extraction & Masking ---
    feats, masked_text = extractor.extract_all(email.text)
    
    # --- Step 2: Preprocessing ---
    clean_text = preprocessor.full_pipeline(masked_text)
    
    # --- Step 3: Baseline Inference (Random Forest) ---
    tfidf_feat = vectorizer.transform([clean_text]).toarray()
    custom_feat = np.array(list(feats.values())).reshape(1, -1)
    X_rf = np.hstack((tfidf_feat, custom_feat))
    
    rf_prob = float(rf_model.predict_proba(X_rf)[0][1])
    
    # --- Step 4: Advanced Inference (Bi-LSTM) ---
    lstm_prob = float(lstm_engine.predict([clean_text])[0][0])
    
    # --- Step 5: Weighted Consensus Logic (v2.2 Calibration) ---
    # We give the LSTM 60% weight and RF 40% weight.
    final_prob = (rf_prob * 0.4) + (lstm_prob * 0.6)
    
    # --- Step 6: Tiered Threat Categorization (Calibrated) ---
    # Increased Clean threshold to 0.45 to reduce false positives on real emails.
    if final_prob < 0.45:
        prediction = "Clean (Ham)"
        threat_level = "Low"
    elif final_prob < 0.75:
        prediction = "Suspicious (Review Required)"
        threat_level = "Medium"
    else:
        prediction = "Phishing (High Risk)"
        threat_level = "High"
    
    # Special Case: If models significantly disagree (e.g., 0% vs 90%), 
    # we always mark as Suspicious even if the average is high.
    if abs(rf_prob - lstm_prob) > 0.8:
        prediction = "Suspicious (Model Disagreement)"
        threat_level = "Medium"

    
    return {
        "prediction": prediction,
        "threat_level": threat_level,
        "phishing_probability": final_prob,
        "model_scores": {
            "baseline_rf": rf_prob,
            "advanced_lstm": lstm_prob
        },
        "extracted_features": feats
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

