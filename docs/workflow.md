# Project Workflow: Phishing Email Detection

This document outlines the end-to-end lifecycle of an email being processed by the Phishing Email Detection Framework.

---

## 1. Data Ingestion
- **Input**: The system accepts raw email text, HTML content, or `.eml` files.
- **Source**: In production, this can be triggered by an API call or a live mail server hook.

## 2. Text Normalization (Preprocessing)
- **HTML Stripping**: Using `BeautifulSoup` to remove all `<tags>`, CSS, and scripts, leaving only the readable content.
- **Cleaning**: Converting text to lowercase and removing special characters.
- **NLTK Processing**: 
    - **Tokenization**: Breaking text into individual words.
    - **Stopword Removal**: Filtering out common words (e.g., "the", "is") that don't add semantic value.
    - **Lemmatization**: Reducing words to their dictionary root (e.g., "running" -> "run").

## 3. Feature Extraction & Masking
- **Lexical Analysis**: Counting URLs, IP addresses, and email addresses using Regular Expressions (Regex).
- **Security Masking**: Replacing sensitive data with tokens (e.g., `http://malicious.com` -> `<URL>`). This prevents the model from "memorizing" specific domains.
- **Semantic Analysis**: Calculating an **Urgency Score** based on the density of threat keywords (e.g., "urgent", "verify", "suspended").

## 4. Vectorization
- **TF-IDF Transform**: The cleaned and masked text is converted into a numerical matrix using *Term Frequency-Inverse Document Frequency*. This weights important words higher and frequent, unimportant words lower.

## 5. Inference (Prediction)
- **Feature Concatenation**: The TF-IDF vectors are combined with the Lexical and Urgency scores.
- **Model Scoring**: The concatenated feature set is passed into the **Random Forest** or **Bi-LSTM** model.
- **Result**: The model outputs a probability score (0.0 to 1.0) and a final label ("Phishing" or "Ham").

## 6. API Response
- The system returns a structured JSON object containing:
    - The final classification.
    - The calculated probability.
    - A breakdown of extracted Indicators of Compromise (IoCs).
