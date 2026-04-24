# Phishing Email Detection Framework

An NLP-driven framework to detect phishing emails and extract Indicators of Compromise (IoCs).

## Project Overview
This project leverages Natural Language Processing (NLP) to distinguish between legitimate (Ham) and malicious (Phishing) emails. It uses a combination of lexical, structural, and semantic features to train high-accuracy classifiers.

## Architecture
- **Data Pipeline**: Ingests and cleans email data from Enron and PhishTank.
- **Feature Extraction**: Uses Regex and NLP to isolate threat intelligence.
- **Classification Engine**: Combines traditional ML baselines with Bi-LSTM deep learning models.
- **Deployment**: Served via FastAPI for real-time inference.

## Documentation
For detailed information on the project's internal workings, please refer to the following documents:
- [Workflow](docs/workflow.md): Step-by-step processing of emails.
- [Code Explanation](docs/code_explanation.md): Detailed breakdown of every module.
- [Architecture](docs/architecture.md): High-level system design and component diagrams.
- [Tech Justification](docs/tech_justification.md): Why we chose our technology stack.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run preprocessing:
   ```bash
   python src/preprocessing/data_pipeline.py
   ```
3. Train the model:
   ```bash
   python src/classification/train.py
   ```
4. Start the API:
   ```bash
   uvicorn src.api.main:app --reload
   ```
