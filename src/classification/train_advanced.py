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
    print("Loading real-world datasets (Enron & Nazario)...")
    
    try:
        enron_df = pd.read_csv("data/Enron.csv")
        nazario_df = pd.read_csv("data/Nazario.csv")
    except FileNotFoundError as e:
        print(f"Error: Dataset not found. {e}")
        return

    # Standardize columns
    enron_df = enron_df[['body', 'label']]
    nazario_df = nazario_df[['body', 'label']]
    
    # Ensure balance (Take 5000 from each or available min)
    min_samples = min(len(enron_df), len(nazario_df), 5000)
    print(f"Sampling {min_samples} emails from each dataset for a balanced set of {min_samples*2} total.")
    
    enron_sample = enron_df.sample(min_samples, random_state=42)
    nazario_sample = nazario_df.sample(min_samples, random_state=42)
    
    df = pd.concat([enron_sample, nazario_sample]).reset_index(drop=True)
    
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

