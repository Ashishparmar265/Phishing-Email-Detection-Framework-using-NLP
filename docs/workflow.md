# Project Workflow: Phishing Email Detection (Evolved v2)

This document outlines the end-to-end lifecycle of an email, highlighting how the system has evolved from a linear pipeline to a parallelized, dual-inference engine.

---

## 1. Data Ingestion
- **Input**: Raw email text, HTML content, or `.eml` files.
- **Source**: API calls (FastAPI) or live stream simulation.

## 2. Text Normalization (Preprocessing)
- **[Legacy]**: Processed emails synchronously one-by-one.
- **[Current]**: Uses **Parallel Preprocessing (Joblib)**. This distributes the load across all available CPU cores, enabling real-time normalization even under high traffic.
- **Steps**:
    - **HTML Stripping**: `BeautifulSoup` removes tags/scripts.
    - **Cleaning**: Lowercase conversion & non-alpha removal.
    - **NLTK Processing**: Tokenization, Stopword Filtering, and Lemmatization.

## 3. Feature Extraction & Masking
- **Lexical Analysis**: Regex-based counting of URLs, IPs, and Emails.
- **Security Masking**: Sensitive data replacement with tokens (e.g., `<URL>`).
- **Semantic Analysis**: Density calculation of "Urgency" keywords.

## 4. Vectorization (Baseline Path)
- **TF-IDF Transform**: Converts masked text into numerical weight matrices for the Random Forest model.

## 5. Dual-Path Inference (Prediction)
The system has transitioned from a single model to a **Consensus Path**:

| Step | [V1] Baseline Path | [V2] Advanced Path |
| :--- | :--- | :--- |
| **Input** | TF-IDF + Lexical Features | Raw Cleaned & Tokenized Text |
| **Model** | **Random Forest** | **Bi-LSTM (Deep Learning)** |
| **Strength** | Fast & Interpretable | Contextual & Semantic |

- **Consensus Logic**: The API runs both paths and selects the **maximum probability** to ensure a "Security First" posture.

## 6. API Response
- The system returns an enriched JSON object:
    - **Consensus Prediction**: Final label based on the highest risk score.
    - **Probability**: The risk level (0.0 to 1.0).
    - **Model Breakdown**: Individual scores from RF and LSTM.
    - **IoC Breakdown**: List of extracted URLs, IPs, and urgency indicators.

