import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

from src.preprocessing.data_pipeline import DataPreprocessor
from src.extraction.feature_extractor import FeatureExtractor

def train_baseline_model(data_path="data/phishing_emails.csv"):
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    preprocessor = DataPreprocessor()
    extractor = FeatureExtractor()
    
    print("Preprocessing and Feature Extraction...")
    # This is a simplified version; in a real scenario, we'd use parallel processing
    processed_texts = []
    custom_features = []
    
    for text in df['body_text']:
        # Extract features first (on raw text)
        feats, masked_text = extractor.extract_all(text)
        # Preprocess the masked text
        clean_text = preprocessor.full_pipeline(masked_text)
        
        processed_texts.append(clean_text)
        custom_features.append(list(feats.values()))
    
    df['processed_text'] = processed_texts
    custom_features = np.array(custom_features)
    
    # Vectorization
    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_tfidf = vectorizer.fit_transform(df['processed_text']).toarray()
    
    # Combine TF-IDF with custom features
    X = np.hstack((X_tfidf, custom_features))
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Baseline...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save models
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/rf_model.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    print("Models saved to models/ directory.")

if __name__ == "__main__":
    train_baseline_model()
