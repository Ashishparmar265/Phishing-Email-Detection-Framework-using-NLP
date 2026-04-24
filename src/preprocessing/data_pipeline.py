import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class DataPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        # Add custom stopwords if necessary (e.g., 'subject', 're', 'fw')
        self.stop_words.update(['subject', 're', 'fw', 'http', 'https', 'www'])

    def strip_html(self, text):
        """Removes HTML tags and returns plain text."""
        if not text:
            return ""
        soup = BeautifulSoup(text, "lxml")
        return soup.get_text(separator=' ')

    def clean_text(self, text):
        """Basic text cleaning: lowercase, remove non-alpha, and extra whitespace."""
        text = text.lower()
        # Remove non-alphanumeric characters but keep tokens like <URL> etc (handled later)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def tokenize_and_lemmatize(self, text):
        """Tokenizes text, removes stopwords, and applies lemmatization."""
        tokens = word_tokenize(text)
        cleaned_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]
        return " ".join(cleaned_tokens)

    def full_pipeline(self, text):
        """Runs the complete preprocessing pipeline."""
        text = self.strip_html(text)
        text = self.clean_text(text)
        text = self.tokenize_and_lemmatize(text)
        return text

if __name__ == "__main__":
    # Example usage
    sample_email = """
    <html>
        <body>
            <h1>Urgent Action Required!</h1>
            <p>Please click <a href="http://malicious.com">here</a> to verify your account.</p>
        </body>
    </html>
    """
    preprocessor = DataPreprocessor()
    processed = preprocessor.full_pipeline(sample_email)
    print(f"Original: {sample_email}")
    print(f"Processed: {processed}")
