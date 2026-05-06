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
    
    try:
        if os.path.exists("data/phishing_email_large.csv"):
            print("Using large compilation dataset (63k+ emails).")
            df_combined = pd.read_csv("data/phishing_email_large.csv")
            # The columns are 'tipo' (label) and 'mensaje' (body)
            df_combined = df_combined.rename(columns={'tipo': 'label', 'mensaje': 'body'})
            # Map 'ham' to 0 and 'phishing' to 1
            df_combined['label'] = df_combined['label'].map({'ham': 0, 'phishing': 1})
            # Drop any NaNs
            df_combined = df_combined.dropna(subset=['body', 'label'])
        elif os.path.exists("data/phishing_emails.csv"):
            print("Using phishing_emails.csv.")
            df_combined = pd.read_csv("data/phishing_emails.csv")
            if 'body_text' in df_combined.columns:
                df_combined = df_combined.rename(columns={'body_text': 'body'})
            df_combined = df_combined[['body', 'label']]
        else:
            print("Error: No datasets found in data/ directory.")
            return
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return
    
    # Separate into Ham (0) and Phishing (1) to fix the bias issue
    ham_df = df_combined[df_combined['label'] == 0]
    phish_df = df_combined[df_combined['label'] == 1]
    
    # Increase samples for baseline as well
    max_per_class = 15000
    min_samples = min(len(ham_df), len(phish_df), max_per_class)
    print(f"Total available - Ham: {len(ham_df)}, Phishing: {len(phish_df)}")
    print(f"Sampling exactly {min_samples} of each for a balanced set of {min_samples*2} total.")
    
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

