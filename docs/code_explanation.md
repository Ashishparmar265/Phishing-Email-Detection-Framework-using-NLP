# Codebase Explanation (Evolved v2)

This document provides a detailed breakdown of every module, including the historical baseline and the current optimized implementation.

---

## 1. `src/preprocessing/data_pipeline.py`
- **Purpose**: Cleans raw, "noisy" email data.
- **Key Class**: `DataPreprocessor`
    - `strip_html()`: Extracts text using `lxml`.
    - `full_pipeline()`: Orchestrates the normalization flow.

## 2. `src/extraction/feature_extractor.py`
- **Purpose**: Extracts manual security indicators.
- **Key Class**: `FeatureExtractor`
    - **Indicator Counting**: URLs, IPs, and Emails.
    - **Security Masking**: Replaces sensitive data with generic tokens to prevent "overfitting" on specific malicious domains.
    - **Urgency Scoring**: Measures the density of pressure keywords.

## 3. `src/classification/train_advanced.py` (Current)
- **Evolution**: Replaced the original `train.py` for advanced modeling.
- **Optimization**:
    - **Parallel Preprocessing**: Uses `joblib.Parallel` and `delayed` to run text normalization across all CPU cores.
    - **Progress Tracking**: Integrated `tqdm` to provide visual feedback during long-running tasks.
- **Logic**: Trains the Bi-LSTM model on real-world datasets (Enron & Nazario).

## 4. `src/classification/lstm_model.py`
- **Purpose**: Defines the Deep Learning engine.
- **Architecture**:
    - **Bi-Directional LSTM**: Captures long-term dependencies in sentence structure.
    - **Tokenizer Integration**: Handles its own text-to-sequence mapping for high-fidelity semantic learning.

## 5. `src/api/main.py` (Current)
- **Evolution**: Upgraded from a single-model server to a **Consensus Engine**.
- **Consensus Logic**:
    - Loads both the **Random Forest** and **Bi-LSTM** models at startup.
    - Performs dual-inference and selects the highest risk score for the final prediction.
- **Technology**: `FastAPI` providing high-concurrency, asynchronous endpoints.

## 6. `src/utils/data_loader.py` (Development)
- **Purpose**: Utility for generating synthetic data.
- **Note**: Used primarily in the early stages (V1) for pipeline validation. V2 uses the real-world Enron and Nazario datasets for high-accuracy training.

## 7. `src/utils/setup_nltk.py`
- **Purpose**: Dependency management.
- **Function**: Automatically downloads the necessary NLTK datasets (`punkt`, `wordnet`, `stopwords`) to ensure the environment is ready for deployment.

