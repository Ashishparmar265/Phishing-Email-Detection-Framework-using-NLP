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

The system now uses two models instead of one, making predictions more reliable.

| Step | Baseline Path | Advanced Path |
| :--- | :--- | :--- |
| **Input** | TF-IDF + Extracted Features | Cleaned & Tokenized Text |
| **Model** | **Random Forest** | **Bi-LSTM (Deep Learning)** |
| **Strength** | Fast and explainable | Context-aware and semantic |

**How it works:**

- Both models process the same email at the same time  
- Each model produces a probability score  
- The system selects the **higher score** as the final decision  

This "max probability" approach ensures a **security-first strategy**, reducing the chances of missing a phishing attempt.

---

## 6. API Response

After processing, the system returns a detailed JSON response.

**It includes:**

- **Final Prediction**  
  The result based on the consensus of both models  

- **Probability Score**  
  A value between 0.0 and 1.0 indicating risk level  

- **Model Breakdown**  
  Individual scores from:
  - Random Forest  
  - Bi-LSTM  

- **Indicators of Compromise (IoC)**  
  Extracted details such as:
  - URLs  
  - IP addresses  
  - Urgency signals  

---

## Final Summary

The workflow is designed to be:
- **Efficient** → Parallel processing reduces latency  
- **Accurate** → Combines traditional ML and deep learning  
- **Transparent** → Provides detailed outputs for analysis  

Overall, the system has evolved into a robust pipeline that can handle real-world email traffic while maintaining high detection accuracy.
