import requests
import json

def test_predict():
    url = "http://localhost:8000/predict"
    
    test_emails = [
        {
            "text": "Urgent: Your account was suspended. Please click http://phish-secure.com/verify to verify your identity.",
            "label": "Phishing"
        },
        {
            "text": "Hi, are we still meeting for lunch today at the Italian place?",
            "label": "Ham"
        }
    ]
    
    for email in test_emails:
        print(f"\nTesting email: {email['text'][:50]}...")
        try:
            response = requests.post(url, json={"text": email['text']})
            result = response.json()
            print(f"Prediction: {result['prediction']}")
            print(f"Threat Level: {result['threat_level']}")
            print(f"Probability: {result['phishing_probability']:.2f}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_predict()
