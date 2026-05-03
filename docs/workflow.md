# Project Workflow: Phishing Email Detection

This document explains how an email moves through the system, from input to final prediction. It also highlights how the workflow has improved over time—from a simple linear pipeline to a faster, parallel, dual-model system.

---

## 1. Data Ingestion

**What happens here:**  
This is where the system receives the email data.

- **Input formats:**
  - Raw text  
  - HTML content  
  - `.eml` files  

- **Source:**
  - API requests (via FastAPI)  
  - Simulated live email streams  

This stage acts as the entry point for all incoming data.

---

## 2. Text Normalization (Preprocessing)

Before any analysis, the email content is cleaned and standardized.

**How it evolved:**

- **Earlier version:**  
  Emails were processed one at a time (synchronously), which was slower.

- **Current version:**  
  Uses **parallel preprocessing (Joblib)** to process multiple emails at once using all CPU cores.  
  This allows the system to handle high traffic efficiently.

**Key steps involved:**

- **HTML Stripping**  
  Removes tags and scripts using BeautifulSoup  

- **Cleaning**  
  Converts text to lowercase and removes unnecessary characters  

- **NLTK Processing**  
  - Tokenization  
  - Stopword removal  
  - Lemmatization  

This ensures the data is clean, consistent, and ready for analysis.

---

## 3. Feature Extraction & Masking

At this stage, the system extracts useful signals from the email.

- **Lexical Analysis**  
  Counts elements such as:
  - URLs  
  - IP addresses  
  - Email addresses  

- **Security Masking**  
  Replaces sensitive data with placeholders (e.g., `<URL>`)  
  This prevents the model from memorizing specific malicious patterns.

- **Semantic Analysis**  
  Measures how strongly the email uses urgency-based language (e.g., “urgent”, “act now”).

---

## 4. Vectorization (Baseline Path)

For the baseline model, the processed text is converted into numerical form.

- **TF-IDF Transformation**  
  Converts text into weighted numerical vectors  
  These vectors are then used by the Random Forest model for prediction  

---

## 5. Dual-Path Inference (Prediction)

The system uses two models working in parallel to calculate a weighted risk score.

| Step | Baseline Path | Advanced Path |
| :--- | :--- | :--- |
| **Input** | TF-IDF + Extracted Features | Cleaned & Tokenized Text |
| **Model** | **Random Forest** | **Bi-LSTM (Deep Learning)** |
| **Strength** | Fast and explainable | Context-aware and semantic |

**Consensus Mechanism (V2.2):**
- **Parallel Processing**: Both models analyze the email simultaneously.
- **Weighted Average**: The system calculates a combined score (40% Random Forest / 60% Bi-LSTM).
- **Safety Override**: If the models disagree by more than 80%, the system automatically flags the email as "Suspicious (Model Disagreement)" for human review.

---

## 5.5 Cybersecurity Payload Heuristic

To eliminate false positives caused by "Domain Shift" (where old clean data differs from modern clean data), a hard security rule is applied:

**The Rule:** If an email has **0 URLs**, **0 IP Addresses**, and **0 Reply-To emails**, it cannot deliver a malicious payload. 

In this case, the system forcibly caps the risk at **20% (Clean)**, ensuring that safe, text-only modern emails are not accidentally blocked.

---

## 6. API Response (Categorization)

The final probability is mapped to one of three clear threat levels shown in the dashboard:

- **Clean (Ham)**: Probability < 0.45 (Green Badge)
- **Suspicious (Review Required)**: Probability 0.45 - 0.75 (Orange Badge)
- **Phishing (High Risk)**: Probability > 0.75 (Red Badge)

The API returns a detailed JSON response including the final prediction, threat level, and individual model scores.

---

## Final Summary

The workflow is designed to be:
- **Efficient** → Parallel processing reduces latency  
- **Accurate** → Combines traditional ML and deep learning  
- **Robust** → Heuristic filters prevent false positives on modern text
- **Transparent** → Provides detailed outputs for analysis  

Overall, the system has evolved into a robust pipeline that can handle real-world email traffic while maintaining high detection accuracy.

