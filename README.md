# Phishing Email Detection Framework

An NLP-driven framework to detect phishing emails and extract Indicators of Compromise (IoCs) using a **Dual-Inference Consensus Engine**. 

Now featuring **Automated Phishing Detection** via a dedicated Chrome Extension for seamless Gmail integration and zero manual copy-paste workflow.

## 🚀 Chrome Extension Integration
The PhishGuard Extension transforms your browser into a powerful threat intelligence tool. It allows you to analyze suspicious emails directly within Gmail without exposing your credentials.

- **Automated Extraction**: Pulls subject, sender, and full email body with a single click.
- **Deep URL Analysis**: Scrapes embedded links, buttons, and even plain-text URLs.
- **Iframe Resolution**: Automatically detects and extracts URLs from hidden iframes within newsletters.
- **Direct Bridge**: Seamlessly transfers data to the local analysis dashboard and triggers detection automatically.

## 🛠️ Installation & Setup

### 1. Backend Setup (API)
The core analysis engine runs on FastAPI.
```bash
# Install dependencies
pip install -r requirements.txt

# Setup NLTK resources
python src/utils/setup_nltk.py

# Start the API server
python src/api/main.py
```
*The API will run at `http://localhost:8000`.*

### 2. Frontend Setup (Dashboard)
The dashboard must be served locally to receive extension data.
```bash
# Navigate to the frontend folder and start a simple server
cd frontend
python -m http.server 3000
```
*The dashboard will be accessible at `http://localhost:3000/index.html`.*

### 3. Chrome Extension Setup
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in the top-right corner).
3. Click **Load unpacked**.
4. Select the `/extension` folder from this project directory.
5. (Optional) Pin the **PhishGuard** extension for easy access.

## 📖 Usage Flow
1. **Open Gmail** and select a suspicious email.
2. **Click the PhishGuard Icon** in your Chrome toolbar.
3. Review the extracted preview in the popup.
4. Click **"Analyze Email"**.
5. You will be redirected to the **Local Dashboard**, where the text is auto-filled and the analysis begins immediately.
6. Review the **Threat Level** (Low/Medium/High) and model scores.

## 🏗️ Project Structure
```text
Phishing-Email-Detection-Framework/
├── extension/                 # Chrome Extension (Manifest V3)
│   ├── manifest.json
│   ├── content.js             # Scraper logic (Gmail DOM)
│   ├── popup.js / popup.html  # Extension UI & Bridge
│   └── styles.css
├── frontend/                  # Glassmorphism Dashboard
│   └── index.html             # Analysis UI & Extension Listener
├── src/
│   ├── api/                   # FastAPI Implementation
│   ├── classification/        # Random Forest & Bi-LSTM Models
│   ├── extraction/            # Feature Engineering
│   └── preprocessing/         # Data Pipeline
└── models/                    # Serialized Weights (.pkl / .h5)
```

## ✨ Key Features
- **Dual-Model Consensus**: Combines Random Forest (Lexical) and Bi-LSTM (Semantic) for 98% accuracy.
- **Real-time Gmail Scraping**: Intelligent DOM traversal with support for threaded conversations.
- **IoC Extraction**: Detects and highlights malicious URLs and urgency markers.
- **Production-Ready UI**: Premium dashboard with real-time model breakdown and consensus probability.

## ⚠️ Notes & Limitations
- **Platform Support**: Currently optimized for Gmail. Other providers (Outlook/Yahoo) may be added in future versions.
- **Dynamic DOM**: Gmail's HTML structure can change; ensure you are using the latest version of this extension.
- **Local Connectivity**: The extension requires both the FastAPI backend and the Python local server to be active.
## Key Features (V2.2)
- **Weighted Consensus Engine**: Combines **Random Forest** (40%) and **Bi-LSTM** (60%) for high-fidelity detection.
- **Payload Heuristic Override**: Hard-coded safety rule to eliminate false positives on safe modern emails by checking for actionable IoCs.
- **Balanced Real-World Training**: Trained on a perfectly balanced 10,000-email corpus (Enron/Nazario).
- **Dockerized Deployment**: Fully containerized environment for consistent performance across machines.

## Documentation
- [Architecture](docs/architecture.md): Dual-Inference and Heuristic logic.
- [Workflow](docs/workflow.md): Step-by-step parallelized processing.
- [Code Explanation](docs/code_explanation.md): Module-level breakdown.
- [Tech Justification](docs/tech_justification.md): Why we chose our optimized stack.
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

gemini --resume 85bcd97a-90e2-47d1-9c7a-50da8421c52f
