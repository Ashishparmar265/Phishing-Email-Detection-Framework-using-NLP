# Phishing Email Detection Framework (v2.0)

An NLP-driven framework to detect phishing emails and extract Indicators of Compromise (IoCs) using a **Dual-Inference Consensus Engine**.

## Project Evolution
The project has evolved from a simple Random Forest baseline (V1) to a sophisticated hybrid system (V2) that combines statistical machine learning with deep learning.

## Architecture (Evolved)
- **Data Pipeline**: Ingests real-world data from Enron and Nazario datasets with **Parallel Preprocessing**.
- **Feature Extraction**: Hybrid extraction of Lexical (URLs/IPs) and Semantic (Urgency) features.
- **Consensus Engine**: Dual-path inference using **Random Forest** and **Bi-LSTM** models for maximum accuracy.
- **Deployment**: Served via FastAPI with a premium Glassmorphism dashboard.

## Documentation
- [Architecture](docs/architecture.md): High-level system design evolution.
- [Workflow](docs/workflow.md): Step-by-step parallelized processing.
- [Code Explanation](docs/code_explanation.md): Module-level breakdown (V1 vs V2).
- [Tech Justification](docs/tech_justification.md): Why we chose our optimized stack.

## Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup NLTK**:
   ```bash
   python src/utils/setup_nltk.py
   ```
3. **Train Advanced Model (V2)**:
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   python src/classification/train_advanced.py
   ```
4. **Start the Integrated API**:
   ```bash
   python src/api/main.py
   ```
5. **Access Dashboard**:
   Open `frontend/index.html` in your browser.

