# System Architecture

The Phishing Email Detection Framework has grown significantly over time. What started as a simple single-model system has now evolved into a **Dual-Inference Consensus Architecture**.

The main idea behind this upgrade is simple: instead of relying on just one model, we combine the strengths of two different approaches. This helps the system make more accurate and reliable decisions when identifying phishing emails.

---

## 1. How the System Evolved

### Phase 1: The Initial Approach
In the beginning, the system used a **Random Forest classifier**. It worked with TF-IDF vectors and a set of manually designed features.

This setup had a few clear advantages:
- It was fast  
- It was easy to understand and explain  

However, it had a limitation, it couldn’t fully capture the deeper meaning or context of email content.

---

### Phase 2: The Current System (Consensus-Based)
To improve accuracy, we introduced a **Bi-LSTM (Bidirectional LSTM)** model alongside the existing Random Forest model.

Now, both models work together using a **consensus-based approach**:

- **Parallel Processing**: Both models analyze the same email at the same time  
- **Maximum Probability Selection**: The system chooses the higher probability score between the two models  

This ensures a **security-first approach**, where even a slight suspicion from either model is taken seriously.

---

## 2. Key Architectural Layers

### A. Ingestion Layer
This is the entry point of the system. It accepts email data in multiple formats such as:
- Plain text  
- HTML  
- JSON  

It is handled through a FastAPI server, which makes the system responsive and scalable.

---

### B. Transformation Layer (Preprocessing)
Before analysis, the input data needs to be cleaned and standardized.

**Recent improvement:**
- Parallel preprocessing using multiple CPU cores, which speeds up both training and real-time predictions  

**Typical operations include:**
- Converting text to lowercase  
- Removing HTML tags  
- Cleaning unnecessary characters  

This layer is stateless and ensures consistent input for all models.

---

### C. Feature Layer (Dual Path Design)

This is where the system extracts meaningful information using two different approaches:

#### Path 1: NLP-Based Features
Uses techniques like TF-IDF or word embeddings to capture the semantic meaning of the text.

#### Path 2: Domain-Specific Features
Extracts handcrafted indicators such as:
- Number of URLs  
- Presence of urgency-related words  
- Structural patterns in the email  

**Result:** A hybrid feature space that combines deep learning insights with practical security signals.

---

### D. Modeling Layer

This layer contains two models working side by side:

#### V1: Random Forest (Baseline)
- Fast  
- Interpretable  
- Reliable for structured signals  

#### V2: Bi-LSTM (Advanced Model)
- Understands sequence and context  
- Captures long-term dependencies in text  

Together, they provide a balanced mix of speed and intelligence.

---

### E. Deployment Layer

This is where everything comes together into a usable system:

- **API Layer**: Built with FastAPI for high performance and asynchronous handling  
- **Frontend Dashboard**: A modern Glassmorphism-based UI that shows results from both models clearly  
- **Containerization**: Docker ensures consistency across environments (same Python version, libraries, datasets)

---

## 3. System Flow Overview

The system processes an email in the following way:

1. The email content is received as input  
2. It goes through preprocessing and cleaning  
3. Features are extracted through both NLP and domain-specific methods  
4. Data is passed to both models:
   - Random Forest  
   - Bi-LSTM  
5. A consensus mechanism selects the higher probability score  
6. The final result is returned as a structured JSON response  

---

## 4. Key Takeaway

This architecture improves phishing detection by:
- Combining **traditional machine learning** and **deep learning**  
- Reducing false negatives (missing threats)  
- Maintaining both **speed and accuracy**  

In short, instead of trusting one model, the system makes a smarter decision by considering multiple perspectives.

---

## 5. Component Diagram

```mermaid
graph TD
    Input[Email Content] --> Clean[Data Pipeline: Parallel Preprocessing]
    Clean --> NLP[NLTK: Tokenize/Lemmatize]
    Clean --> Feat[Feature Extractor: URLs/IPs/Urgency]
    NLP --> Vector[TF-IDF Vectorizer]
    Vector --> Concat[Feature Fusion]
    Feat --> Concat
    Concat --> ModelRF[V1: Random Forest]
    Clean --> ModelLSTM[V2: Bi-LSTM Engine]
    ModelRF --> Consensus[Consensus Logic: Weighted Average]
    ModelLSTM --> Consensus
    Consensus --> Heuristic[Cybersecurity Payload Heuristic]
    Heuristic --> Output[JSON Response: Dual-Score Breakdown + Tiered Label]
```

---

## 6. Phase 3: The Cybersecurity Payload Heuristic (V2.2)

After deploying the dual-inference consensus engine, we identified a critical machine learning flaw: **Domain Shift**. 
- The models were trained on early 2000s energy corporate emails (Enron) and modern phishing emails (Nazario). 
- When confronted with a *modern* safe email (like an Amazon job application), the NLP models flagged it as phishing simply because it used modern tech vocabulary that wasn't present in the Enron dataset.

To solve this fundamentally, we introduced the **Cybersecurity Payload Heuristic** as an absolute override mechanism in the API layer.

### How it Works:
A phishing attack *must* have a payload mechanism to be dangerous.
If the `FeatureExtractor` determines that the email contains:
- `0` URLs (Links)
- `0` IP Addresses
- `0` Email addresses to reply to
- Low Urgency Score (< 0.2)

...then the email is physically incapable of delivering an attack. In this scenario, the API **overrides the NLP consensus** and forcibly caps the phishing probability at **20% (Clean)**. This elegantly marries theoretical Machine Learning with practical Cybersecurity engineering.
