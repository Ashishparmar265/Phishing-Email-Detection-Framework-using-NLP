# Technology Justification & Comparative Analysis (Evolved v2)

This document explains the rationale behind our tech stack, focusing on the evolution from a simple baseline to a high-concurrency consensus engine.

---

## 1. Programming Language: Python 3.x
- **Choice**: Python
- **Why**: Industry standard for NLP and ML. Enables seamless integration between `NLTK`, `Scikit-learn`, and `TensorFlow`.

## 2. Text Processing: NLTK
- **Choice**: NLTK (Natural Language Toolkit)
- **Why**: Provides granular control over tokenization and lemmatization, which is essential for security-focused text analysis where every character (URLs/IPs) matters.

## 3. Modeling: The Consensus Engine (V1 + V2)
- **Approach**: **Hybrid Baseline + Deep Learning**
- **Why**: 
    - **[V1] Random Forest**: Provides **Explainability**. In cybersecurity, knowing *why* an email was flagged (e.g., high urgency score + 3 URLs) is just as important as the flag itself.
    - **[V2] Bi-LSTM**: Provides **Semantic Context**. It detects patterns in the *way* scammers write, catching deceptive intent even if they avoid common "threat words."
- **Evolution**: By using both in a **Consensus Engine**, we eliminate the "single point of failure" in classification.

## 4. Performance Optimization: Joblib (New in V2)
- **Choice**: **Joblib (Parallel Processing)**
- **Why**: Text preprocessing (HTML stripping, Lemmatization) is CPU-bound. In V1, processing 10k emails took ~10 minutes. In V2, by using **Joblib** to distribute tasks across all 8 CPU cores, we reduced this time by **80%**.

## 5. Feature Vectorization: TF-IDF vs. Embeddings
- **TF-IDF**: Used for the RF model for speed and word-level importance.
- **Keras Embeddings**: Used for the Bi-LSTM to capture high-dimensional semantic relationships.

## 6. Web Framework: FastAPI
- **Choice**: FastAPI
- **Why**: Handles asynchronous requests and provides automatic Swagger documentation. Its speed is critical for real-time email scanning.

## 7. Containerization: Docker
- **Choice**: Docker
- **Why**: Solves "Dependency Hell." Ensures TensorFlow, NLTK data, and all Python libraries are perfectly consistent across development and deployment environments.

