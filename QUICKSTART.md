# Phishing Email Detection Framework - Quickstart Guide

This project uses NLP and Machine Learning to detect and classify phishing emails. It features a dual-model approach (Random Forest + Bi-LSTM) and provides a REST API with a modern web frontend.

## 🚀 Prerequisites

- Python 3.10+ (Tested on Python 3.14)
- Virtual Environment (Recommended)

## 🛠️ Setup Instructions

### 1. Initialize Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# Note: If on Python 3.14+, TensorFlow might be skipped. 
# The system will automatically fall back to the Random Forest model.
```

### 3. Setup NLTK Data
Download the required NLP models and stopword lists:
```bash
python3 src/utils/setup_nltk.py
```

## 📈 Model Training

### Generate Synthetic Data & Train Baseline
To get the system running immediately with a baseline model:
```bash
PYTHONPATH=. .venv/bin/python src/utils/data_loader.py
PYTHONPATH=. .venv/bin/python src/classification/train.py
```
This creates `models/rf_model.pkl` and `models/vectorizer.pkl`.

## 🖥️ Running the Application

### 1. Start the FastAPI Server
```bash
PYTHONPATH=. .venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```
The API will be available at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.

### 2. Launch the Frontend
Simply open the `frontend/index.html` file in any modern web browser.
- Ensure the API server is running first.
- Paste an email into the text area and click **Analyze Email**.

### 3. Run a Quick CLI Test
In a new terminal, run the provided test script:
```bash
PYTHONPATH=. .venv/bin/python src/test_api.py
```

## 📂 Project Structure

- `src/api/`: FastAPI implementation and consensus logic.
- `src/classification/`: ML model architectures (Random Forest & LSTM).
- `src/extraction/`: Feature extraction (URLs, IPs, Urgency).
- `src/preprocessing/`: Text cleaning and tokenization pipeline.
- `frontend/`: HTML/CSS/JS web interface.
- `models/`: Trained model weights and metadata.

## ⚠️ Note on Deep Learning (TensorFlow)
If TensorFlow is installed and a model is trained via `src/classification/train_advanced.py`, the API will automatically perform a weighted consensus between the Baseline and Advanced models for higher accuracy. If TensorFlow is missing, it safely falls back to the Random Forest model.

 gemini --resume 85d60c3f-0f23-4b48-a03e-d7ec559b2f7c