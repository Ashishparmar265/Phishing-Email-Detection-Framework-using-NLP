# Codebase Explanation

This document walks through the structure of the codebase and explains what each module does. It also highlights how the system has evolved from its initial version to the current, more optimized implementation.

---

## 1. `src/preprocessing/data_pipeline.py`

**What it does:**  
This module is responsible for cleaning and preparing raw email data before it is used by the models. Since real-world emails can be messy (HTML, special characters, etc.), this step ensures consistency.

**Main class:** `DataPreprocessor`

- `strip_html()`  
  Extracts readable text from HTML content using `lxml`.

- `full_pipeline()`  
  Runs the complete preprocessing workflow, including cleaning, normalization, and formatting.

---

## 2. `src/extraction/feature_extractor.py`

**What it does:**  
This module focuses on extracting meaningful security-related features from emails. These features help the model detect suspicious patterns beyond just text meaning.

**Main class:** `FeatureExtractor`

- **Indicator Counting**  
  Counts elements like:
  - URLs  
  - IP addresses  
  - Email addresses  

- **Security Masking**  
  Replaces sensitive or specific data (like domains) with generic placeholders.  
  This prevents the model from overfitting to particular known phishing sources.

- **Urgency Scoring**  
  Measures how strongly the email uses pressure tactics (e.g., “urgent”, “act now”, etc.).

---

## 3. `src/classification/train_advanced.py` (Current)

**What it does:**  
This is the upgraded training pipeline used for the advanced model. It replaces the earlier `train.py` used in the initial version.

**Key improvements:**

- **Parallel Preprocessing**  
  Uses `joblib.Parallel` and `delayed` to process multiple emails at the same time using all CPU cores.  
  This significantly reduces training time.

- **Progress Tracking**  
  Uses `tqdm` to show a progress bar, making long training runs easier to monitor.

**Overall role:**  
Trains the Bi-LSTM model using real-world datasets like Enron and Nazario, which improves the model’s ability to generalize.

---

## 4. `src/classification/lstm_model.py`

**What it does:**  
This module defines the deep learning model used in the system.

**Key components:**

- **Bi-Directional LSTM**  
  Allows the model to understand context from both directions in a sentence, improving detection of subtle phishing patterns.

- **Tokenizer Integration**  
  Handles converting raw text into sequences that the model can understand, ensuring consistent and meaningful input representation.

---

## 5. `src/api/main.py` (Current)

**What it does:**  
This is the main API layer that connects the models to the outside world.

**What changed:**  
Earlier, the API used only one model. Now it acts as a **Consensus Engine**.

**How it works:**

- Loads both:
  - Random Forest model  
  - Bi-LSTM model  

- Runs both models on the same input  
- Selects the higher risk score as the final prediction  

**Technology used:**  
Built with `FastAPI`, which allows:
- High performance  
- Asynchronous request handling  
- Scalability  

---

## 6. `src/utils/data_loader.py` (Development)

**What it does:**  
This module was used during early development to generate synthetic data for testing and validating the pipeline.

**Note:**  
It was mainly useful in earlier version of the system.
The current system relies on real datasets like Enron and Nazario for better accuracy.

---

## 7. `src/utils/setup_nltk.py`

**What it does:**  
This module ensures that all required NLTK resources are available.

**Functionality:**

- Automatically downloads:
  - `punkt`  
  - `wordnet`  
  - `stopwords`  

This helps avoid setup issues and ensures the environment is ready to run the preprocessing steps without manual intervention.

---

## Final Note

Overall, the codebase is designed with a clear separation of responsibilities:
- Preprocessing handles raw input  
- Feature extraction adds security-specific insights  
- Models perform classification  
- The API ties everything together  

The transition from a simple pipeline to a more optimized and parallelized system has significantly improved both performance and accuracy.
