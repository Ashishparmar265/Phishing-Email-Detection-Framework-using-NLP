# Technology Justification & Comparative Analysis

This document explains why specific technologies were chosen for the Phishing Email Detection Framework and evaluates them against alternatives.

---

## 1. Programming Language: Python 3.x
- **Choice**: Python
- **Why**: Python is the industry standard for NLP and Machine Learning. It has a rich ecosystem of libraries (`NLTK`, `Scikit-learn`, `TensorFlow`) and allows for rapid prototyping.
- **Alternatives**: C++ (too slow to develop), Go (limited ML libraries), Java (verbose).

## 2. Text Processing: NLTK vs. Spacy
- **Choice**: NLTK (Natural Language Toolkit)
- **Why**: NLTK is highly granular and excellent for research and educational blueprints. It provides precise control over tokenization and lemmatization, which is crucial for identifying specific phishing artifacts.
- **Alternatives**: **Spacy** is faster and better for "industrial" NLP, but NLTK was chosen for this blueprint to align with academic and security research standards.

## 3. Modeling: Random Forest & Bi-LSTM
- **Choice**: Hybrid (Baseline + Sequential)
- **Why**: 
    - **Random Forest**: It is highly robust to outliers and provides feature importance (explainability), which is critical in cybersecurity.
    - **Bi-LSTM**: Phishing attempts rely on the "flow" of a sentence. A Recurrent Neural Network like LSTM remembers the beginning of a sentence when it reaches the end, making it much better at detecting deceptive urgency than simple keyword matching.
- **Alternatives**: **SVM** (good, but less explainable), **Transformer/BERT** (better performance, but requires massive compute resources and data).

## 4. Feature Vectorization: TF-IDF vs. Word2Vec
- **Choice**: TF-IDF (for baseline)
- **Why**: TF-IDF is computationally efficient and works exceptionally well for classification tasks where specific "threat words" (e.g., "password", "unauthorized") have high predictive power.
- **Alternatives**: **Word2Vec** or **GloVe** capture semantic meaning better but can be over-sensitive to noise in raw email text.

## 5. Web Framework: FastAPI vs. Flask/Django
- **Choice**: FastAPI
- **Why**: FastAPI is built on modern Python type hints and is significantly faster than Flask (using `Uvicorn`/`Starlette`). It automatically generates OpenAPI documentation (`/docs`), which is essential for security teams integrating the API.
- **Alternatives**: **Flask** (standard but slower), **Django** (too heavy for a simple microservice).

## 6. Containerization: Docker
- **Choice**: Docker
- **Why**: ML environments are notorious for "dependency hell" (conflicting library versions). Docker ensures that the specific versions of TensorFlow and NLTK data work exactly the same way in production as they do in development.
