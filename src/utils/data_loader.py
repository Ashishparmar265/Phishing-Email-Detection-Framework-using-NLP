import pandas as pd
import numpy as np
import os

def generate_synthetic_data(output_path="data/phishing_emails.csv", num_samples=1000):
    """Generates a synthetic dataset for development."""
    phishing_templates = [
        "Urgent: Your account {id} was suspended. Please click {url} to verify.",
        "Security Alert: Unauthorized access detected from {ip}. Verify now: {url}",
        "Invoice {id} is attached. Please review it at {url}.",
        "Dear customer, your password for {email} has expired. Reset here: {url}",
        "Limited time offer! Get a free gift at {url}. Don't miss out!"
    ]
    
    ham_templates = [
        "Meeting reminder for tomorrow at 10 AM.",
        "Hi, can you send me the report for the previous quarter?",
        "Lunch today? Let's go to the Italian place.",
        "The project update is attached. Please review and let me know.",
        "Happy Birthday! Hope you have a great day."
    ]
    
    data = []
    for i in range(num_samples):
        is_phishing = np.random.choice([0, 1])
        if is_phishing:
            template = np.random.choice(phishing_templates)
            email_text = template.format(
                id=np.random.randint(1000, 9999),
                url=f"http://phish-{np.random.randint(100, 999)}.com/verify",
                ip=f"192.168.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}",
                email=f"user{np.random.randint(1, 100)}@example.com"
            )
        else:
            email_text = np.random.choice(ham_templates)
        
        data.append({
            'email_id': i,
            'body_text': email_text,
            'label': is_phishing
        })
    
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {num_samples} samples at {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()
