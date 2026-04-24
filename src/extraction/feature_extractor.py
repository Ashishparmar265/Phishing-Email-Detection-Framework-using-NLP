import re
from urllib.parse import urlparse

class FeatureExtractor:
    def __init__(self):
        # Regex patterns
        self.url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Urgency keywords from document
        self.urgency_keywords = [
            "immediate action", "account suspended", "verify identity", 
            "invoice attached", "urgent", "password", "verify", "suspend",
            "limited time", "security alert", "unauthorized access"
        ]

    def extract_lexical_features(self, text):
        """Extracts counts of URLs, IPs, and email addresses."""
        urls = re.findall(self.url_pattern, text)
        ips = re.findall(self.ip_pattern, text)
        emails = re.findall(self.email_pattern, text)
        
        # Check for @ in URL (common phishing tactic)
        at_in_url = any('@' in url for url in urls)
        
        return {
            'url_count': len(urls),
            'ip_count': len(ips),
            'email_count': len(emails),
            'at_in_url': int(at_in_url)
        }

    def mask_sensitive_info(self, text):
        """Replaces URLs, IPs, and Emails with generic tokens."""
        text = re.sub(self.url_pattern, '<URL>', text)
        text = re.sub(self.ip_pattern, '<IP>', text)
        text = re.sub(self.email_pattern, '<EMAIL>', text)
        return text

    def get_urgency_score(self, text):
        """Calculates the density of urgency keywords."""
        text = text.lower()
        count = sum(1 for word in self.urgency_keywords if word in text)
        return count / (len(text.split()) + 1)

    def extract_all(self, text):
        """Runs all extraction and returns a feature dictionary + masked text."""
        lexical = self.extract_lexical_features(text)
        urgency_score = self.get_urgency_score(text)
        masked_text = self.mask_sensitive_info(text)
        
        features = {**lexical, 'urgency_score': urgency_score}
        return features, masked_text

if __name__ == "__main__":
    sample = "Urgent: Your account was accessed from 192.168.1.1. Click http://secure-login.com to verify."
    extractor = FeatureExtractor()
    features, masked = extractor.extract_all(sample)
    print(f"Features: {features}")
    print(f"Masked: {masked}")
