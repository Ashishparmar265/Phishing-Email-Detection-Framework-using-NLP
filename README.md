# Phishing Email Detection Framework

An NLP-driven framework to detect phishing emails and extract Indicators of Compromise (IoCs) using a **Dual-Inference Consensus Engine**.

## Key Features (V2.2)
- **Weighted Consensus Engine**: Combines **Random Forest** (40%) and **Bi-LSTM** (60%) for high-fidelity detection.
- **Payload Heuristic Override**: Hard-coded safety rule to eliminate false positives on safe modern emails by checking for actionable IoCs.
- **Balanced Real-World Training**: Trained on a perfectly balanced 10,000-email corpus (Enron/Nazario).
- **Dockerized Deployment**: Fully containerized environment for consistent performance across machines.

## Documentation
- [Architecture](docs/architecture.md): Dual-Inference and Heuristic logic.
- [Workflow](docs/workflow.md): Step-by-step parallelized processing.
- [Code Explanation](docs/code_explanation.md): Module-level breakdown (V2.2).
- [Tech Justification](docs/tech_justification.md): Why we chose our optimized stack.

## Setup (Local)
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Setup NLTK**: `python src/utils/setup_nltk.py`
3. **Train Models**:
   ```bash
   python src/classification/train.py          # Baseline
   python src/classification/train_advanced.py # Advanced
   ```
4. **Start API**: `python src/api/main.py`

## Setup (Docker - Recommended)
1. **Build Image**: `docker build -t phishguard-api .`
2. **Run Container**: `docker run -d -p 8000:8000 --name phishguard-container phishguard-api`

## Dashboard
Open `frontend/index.html` in your browser to analyze emails in real-time.

