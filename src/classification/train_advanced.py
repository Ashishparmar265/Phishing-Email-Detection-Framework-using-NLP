import pandas as pd
import numpy as np
import os
import joblib
from tqdm import tqdm
from joblib import Parallel, delayed
from sklearn.model_selection import train_test_split
from src.preprocessing.data_pipeline import DataPreprocessor
from src.extraction.feature_extractor import FeatureExtractor
from src.classification.lstm_model import PhishingLSTM

def process_single_email(text, extractor, preprocessor):
    """Helper function for parallel processing."""
    if not isinstance(text, str):
        text = str(text) if text else ""
    
    # Masking and basic cleaning
    _, masked_text = extractor.extract_all(text)
    clean_text = preprocessor.full_pipeline(masked_text)
    return clean_text

def train_advanced_model():
    print("\n--- Phase 5: Advanced Model Training ---")
    
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
    
    # Increase samples for better generalization, but keep it within time limits
    # 15,000 per class (30,000 total) should be plenty and train quickly on GPU
    max_per_class = 15000
    min_samples = min(len(ham_df), len(phish_df), max_per_class)
    print(f"Total available - Ham: {len(ham_df)}, Phishing: {len(phish_df)}")
    print(f"Sampling exactly {min_samples} of each for a balanced set of {min_samples*2} total.")
    
    ham_sample = ham_df.sample(min_samples, random_state=42)
    phish_sample = phish_df.sample(min_samples, random_state=42)
    
    # Combine and shuffle
    df = pd.concat([ham_sample, phish_sample]).sample(frac=1, random_state=42).reset_index(drop=True)

    
    preprocessor = DataPreprocessor()
    extractor = FeatureExtractor()
    
    print(f"\nPreprocessing {len(df)} emails using 8 CPU cores...")
    # Parallel processing with tqdm progress bar
    processed_texts = Parallel(n_jobs=-1)(
        delayed(process_single_email)(text, extractor, preprocessor) 
        for text in tqdm(df['body'], desc="Cleaning & Tokenizing")
    )
    
    X = processed_texts
    y = df['label'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\nInitializing Bi-LSTM Network...")
    lstm = PhishingLSTM(max_words=10000, max_len=150)
    
    print("\nStarting Deep Learning Training...")
    # Training with verbose=1 shows per-epoch progress bars
    lstm.fit(X_train, y_train, epochs=10, batch_size=64)
    
    print("\nSaving Advanced Model...")
    os.makedirs("models", exist_ok=True)
    lstm.save("models/phishing_lstm")
    print("SUCCESS: Advanced model saved to models/phishing_lstm.h5")
    print("SUCCESS: Tokenizer saved to models/phishing_lstm_tokenizer.pkl")

if __name__ == "__main__":
    train_advanced_model()

