import pandas as pd
import numpy as np
import os
import joblib
from tqdm import tqdm
from joblib import Parallel, delayed
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

from src.preprocessing.data_pipeline import DataPreprocessor
from src.extraction.feature_extractor import FeatureExtractor

def process_single_email(text, extractor, preprocessor):
    """Helper function for parallel processing."""
    if not isinstance(text, str):
        text = str(text) if text else ""
    feats, masked_text = extractor.extract_all(text)
    clean_text = preprocessor.full_pipeline(masked_text)
    return clean_text, list(feats.values())

def train_baseline_model():
    print("\n--- Phase 1-3: Baseline Model Training (Retrain) ---")
    print("Loading real-world datasets (Enron & Nazario)...")
    
    try:
        enron_df = pd.read_csv("data/Enron.csv")
        nazario_df = pd.read_csv("data/Nazario.csv")
    except FileNotFoundError as e:
        print(f"Error: Dataset not found. {e}")
        return

    enron_df = enron_df[['body', 'label']]
    nazario_df = nazario_df[['body', 'label']]
    
    # Combine both datasets to pool all available real-world data
    df_combined = pd.concat([enron_df, nazario_df]).reset_index(drop=True)
    
    # Separate into Ham (0) and Phishing (1) to fix the bias issue
    ham_df = df_combined[df_combined['label'] == 0]
    phish_df = df_combined[df_combined['label'] == 1]
    
    min_samples = min(len(ham_df), len(phish_df), 5000)
    print(f"Total available - Ham: {len(ham_df)}, Phishing: {len(phish_df)}")
    print(f"Sampling exactly {min_samples} of each for a perfectly balanced set of {min_samples*2} total.")
    
    ham_sample = ham_df.sample(min_samples, random_state=42)
    phish_sample = phish_df.sample(min_samples, random_state=42)
    
    df = pd.concat([ham_sample, phish_sample]).sample(frac=1, random_state=42).reset_index(drop=True)
    
    preprocessor = DataPreprocessor()
    extractor = FeatureExtractor()
    
    print(f"\nPreprocessing {len(df)} emails using 8 CPU cores...")
    # Parallel processing with tqdm progress bar
    results = Parallel(n_jobs=-1)(
        delayed(process_single_email)(text, extractor, preprocessor) 
        for text in tqdm(df['body'], desc="Cleaning & Extracting Features")
    )
    
    processed_texts = [res[0] for res in results]
    custom_features = np.array([res[1] for res in results])
    
    # Vectorization
    print("\nVectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_tfidf = vectorizer.fit_transform(processed_texts).toarray()
    
    # Combine TF-IDF with custom features
    X = np.hstack((X_tfidf, custom_features))
    y = df['label'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\nTraining Random Forest Baseline...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save models
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/rf_model.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    print("SUCCESS: Baseline models saved to models/rf_model.pkl and models/vectorizer.pkl.")

if __name__ == "__main__":
    train_baseline_model()

