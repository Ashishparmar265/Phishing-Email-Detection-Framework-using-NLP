# Codebase Explanation

This document walks through the structure of the codebase and explains what each module does. It also highlights how the system has evolved from its initial version to the current, more optimized implementation.

---

## 1. `src/preprocessing/data_pipeline.py`

**What it does:**  
This module is responsible for cleaning and preparing raw email data before it is used by the models. Since real-world emails can be messy (HTML, special characters, etc.), this step ensures consistency.

**Main class:** `DataPreprocessor`

- `strip_html()`  
  Extracts readable text from HTML content using `lxml`.

- `full_pipeline()`  
  Runs the complete preprocessing workflow, including cleaning, normalization, and formatting.

---

## 2. `src/extraction/feature_extractor.py`

**What it does:**  
This module focuses on extracting meaningful security-related features from emails. These features help the model detect suspicious patterns beyond just text meaning.

**Main class:** `FeatureExtractor`

- **Indicator Counting**  
  Counts elements like:
  - URLs  
  - IP addresses  
  - Email addresses  

- **Security Masking**  
  Replaces sensitive or specific data (like domains) with generic placeholders.  
  This prevents the model from overfitting to particular known phishing sources.

- **Urgency Scoring**  
  Measures how strongly the email uses pressure tactics (e.g., “urgent”, “act now”, etc.).

---

## 3. `src/classification/train_advanced.py` & `train.py` (V2.2)

**What it does:**  
These modules handle the training of the Bi-LSTM and Random Forest models respectively. 

**Key improvements (V2.2):**
- **Balanced Real-World Data**: Both scripts now use a perfectly balanced 50/50 mix of Enron (Ham) and Nazario (Phishing) datasets.
- **Parallel Preprocessing**: Both scripts utilize multi-core processing to clean and tokenize 10,000+ emails in seconds.
- **Progress Tracking**: Uses `tqdm` for real-time monitoring of the training process.

---

## 4. `src/classification/lstm_model.py`

**What it does:**  
This module defines the deep learning model used in the system.

**Key components:**

- **Bi-Directional LSTM**  
  Allows the model to understand context from both directions in a sentence, improving detection of subtle phishing patterns.

- **Tokenizer Integration**  
  Handles converting raw text into sequences that the model can understand, ensuring consistent and meaningful input representation.

---

## 5. `src/api/main.py` (Current)

**What it does:**  
This is the main API layer that acts as a **Dual-Inference Consensus Engine**.

**Key logic (V2.2):**

- **Consensus Mechanism**: Runs both models and calculates a weighted average (40% RF / 60% LSTM).
- **Cybersecurity Payload Heuristic**: Implements a safety override. If an email has 0 URLs, 0 IPs, and 0 Emails to reply to, it forcibly caps the risk at 20%, preventing "Domain Shift" false positives.
- **Safety Disagreement**: Flags emails where models disagree by > 80% as "Suspicious".

**Technology used:**  
Built with `FastAPI`, providing high performance and asynchronous request handling.

---

## 6. `src/utils/data_loader.py` (Legacy)

**What it does:**  
Used during early development to generate synthetic data.

**Note:**  
The current production system has moved beyond this and relies entirely on the real-world Enron and Nazario corpora for superior accuracy.

---

## 7. `src/utils/setup_nltk.py`

**What it does:**  
This module ensures that all required NLTK resources are available.

**Functionality:**

- Automatically downloads:
  - `punkt`  
  - `wordnet`  
  - `stopwords`  

This helps avoid setup issues and ensures the environment is ready to run the preprocessing steps without manual intervention.

---

## Final Note

The codebase is organized into modular layers:
- **Preprocessing** cleans raw text.
- **Feature Extraction** identifies security signals.
- **Classification** predicts threat probability.
- **API Engine** balances AI insights with hard security heuristics.

This combination of Deep Learning and Cybersecurity rules ensures the system is both intelligent and reliable.

