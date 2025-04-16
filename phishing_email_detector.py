import os  # ⚡ ADD THIS MISSING IMPORT
import imaplib
import email
import time
import re
import tldextract
import joblib  # ⚡ CHANGED FROM sklearn.externals.joblib
from rich.console import Console
from dotenv import load_dotenv

console = Console()
load_dotenv()
EMAIL = os.getenv("EMAIL_ADDR")
PASSWORD = os.getenv("EMAIL_PASS")

# Load your ML model and vectorizer
model = joblib.load("phishing_model.pkl")  # Now using the newly trained model
vectorizer = joblib.load("vectorizer.pkl")  # And the new vectorizer

# ... [rest of your existing code remains exactly the same] ...

# Legitimate domains (can expand)
legit_domains = ["google", "gmail", "microsoft", "yahoo"]

def connect_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    return mail

def check_new_emails(mail):
    status, messages = mail.search(None, 'UNSEEN')
    return messages[0].split()

def parse_email(msg_data):
    msg = email.message_from_bytes(msg_data)
    subject = msg["subject"]
    sender = msg["from"]
    body = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            try:
                body += part.get_payload(decode=True).decode()
            except:
                continue
    return subject, sender, body

def extract_links(text):
    return re.findall(r'(https?://\S+)', text)

def suspicious_link(link):
    domain = tldextract.extract(link).domain
    return domain not in legit_domains

def is_phishing(text):
    features = vectorizer.transform([text])
    prediction = model.predict(features)
    return prediction[0] == 1

def alert(email_data):
    console.print("[bold red]⚠️ Phishing Detected![/bold red]")
    console.print(f"[bold]Subject:[/bold] {email_data['subject']}")
    console.print(f"[bold]From:[/bold] {email_data['from']}")
    if email_data['links']:
        console.print("[bold yellow]Suspicious Links:[/bold yellow]")
        for link in email_data['links']:
            console.print(f"- {link}")

def main():
    mail = connect_email()
    console.print("[green]Started Real-Time Phishing Detector[/green]")

    while True:
        ids = check_new_emails(mail)
        for email_id in ids:
            _, data = mail.fetch(email_id, "(RFC822)")
            subject, sender, body = parse_email(data[0][1])
            links = extract_links(body)
            suspicious_links = [l for l in links if suspicious_link(l)]

            if is_phishing(body) or suspicious_links:
                alert({
                    "subject": subject,
                    "from": sender,
                    "links": suspicious_links
                })

        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    main()
