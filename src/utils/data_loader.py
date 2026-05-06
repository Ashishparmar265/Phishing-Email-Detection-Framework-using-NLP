import pandas as pd
import numpy as np
import os

def generate_synthetic_data(output_path="data/phishing_emails.csv", num_samples=3000):
    """Generates a synthetic dataset for development."""
    phishing_templates = [
        "Urgent: Your account {id} was suspended. Please click {url} to verify.",
        "Security Alert: Unauthorized access detected from {ip}. Verify now: {url}",
        "Invoice {id} is attached. Please review it at {url}.",
        "Dear customer, your password for {email} has expired. Reset here: {url}",
        "Limited time offer! Get a free gift at {url}. Don't miss out!",
        "Dear User, Your system has been infected with malware and sensitive data may have been compromised. Download the security patch immediately: {url} If no action is taken, your files may be deleted permanently. Support Team",
        "Action Required: Your payment of $499.99 for order {id} was successful. If you did not authorize this transaction, cancel it immediately here: {url}",
        "Final notice: Your bank account is restricted. Please update your billing information immediately at {url}",
        "You have received a secure wire transfer. Click {url} to view your receipt.",
        "Bitcoin investment alert! Double your crypto within 24 hours. Deposit here: {url}",
        "Your PayPal account has been limited due to suspicious activity. Verify identity: {url}"
    ]
    
    ham_templates = [
        "Meeting reminder for tomorrow at 10 AM.",
        "Hi, can you send me the report for the previous quarter?",
        "Lunch today? Let's go to the Italian place.",
        "The project update is attached. Please review and let me know.",
        "Happy Birthday! Hope you have a great day.",
        "Check out this interesting article I found: https://en.wikipedia.org/wiki/Machine_learning",
        "The documentation is available at https://docs.python.org/3/ for your reference.",
        "You can find the code repo at https://github.com/example/repo",
        "Let's meet via Zoom: https://zoom.us/j/123456789",
        "Here is the stackoverflow thread discussing this issue: https://stackoverflow.com/questions/123456",
        "For more information, visit our website at https://www.google.com",
        "I've shared the document here: https://docs.google.com/document/d/example/edit",
        "Your Amazon order has shipped. Track your package here: https://amazon.com/track/123",
        "GitHub: A new issue was opened in your repository. View it at https://github.com/example/issues/1",
        "Weekly Newsletter: Here are the top 5 articles you missed this week: https://news.example.com",
        "Reminder: Please submit your timesheet by Friday 5 PM.",
        "Thank you for your purchase! Your receipt is attached.",
        "Are we still on for the 2 PM call? Here is the google meet link: https://meet.google.com/abc-defg-hij"
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
