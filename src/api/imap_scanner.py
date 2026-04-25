import imaplib
import email
from email.header import decode_header
import requests
import time
import os

class IMAPScanner:
    def __init__(self, imap_url, username, password, api_url="http://localhost:8000/predict"):
        self.imap_url = imap_url
        self.username = username
        self.password = password
        self.api_url = api_url

    def connect(self):
        self.mail = imaplib.IMAP4_SSL(self.imap_url)
        self.mail.login(self.username, self.password)
        self.mail.select("inbox")

    def scan_latest(self, num_emails=10):
        print(f"Scanning latest {num_emails} emails...")
        _, messages = self.mail.search(None, "ALL")
        email_ids = messages[0].split()
        
        # Get the last N emails
        latest_email_ids = email_ids[-num_emails:]
        
        for e_id in latest_email_ids:
            _, msg_data = self.mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    print(f"Processing: {subject}")
                    
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    if body:
                        self.analyze_email(body, subject)

    def analyze_email(self, body, subject):
        try:
            response = requests.post(self.api_url, json={"text": body})
            data = response.json()
            if data["prediction"] == "Phishing":
                print(f"⚠️  ALERT: Phishing detected in email: '{subject}'")
                print(f"Probability: {data['phishing_probability']:.2f}")
            else:
                print(f"✅ Clean: '{subject}'")
        except Exception as e:
            print(f"Error calling API: {e}")

    def logout(self):
        self.mail.close()
        self.mail.logout()

if __name__ == "__main__":
    # This is a placeholder for actual credentials
    # In a real scenario, use environment variables
    IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
    EMAIL_USER = os.getenv("EMAIL_USER", "your-email@gmail.com")
    EMAIL_PASS = os.getenv("EMAIL_PASS", "your-app-password")
    
    print("IMAP Scanner initialized. (Configure environment variables to run)")
    # scanner = IMAPScanner(IMAP_SERVER, EMAIL_USER, EMAIL_PASS)
    # scanner.connect()
    # scanner.scan_latest()
    # scanner.logout()
