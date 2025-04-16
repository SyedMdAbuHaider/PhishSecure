from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Corrected training data with equal length arrays
train_data = {
    'text': [
        # Phishing examples
        'Claim your free prize now', 
        'Verify account immediately',
        'You won $1000 gift card', 
        'Security alert: login detected',
        'Click to unlock reward', 
        'Password reset required',
        'Account compromised', 
        'Urgent: suspicious activity',
        'Your Netflix payment failed', 
        'Apple ID login from new device',
        
        # Legitimate examples
        'Meeting at 3pm tomorrow', 
        'Your invoice #12345',
        'Team lunch next Friday', 
        'Subscription renewal notice',
        'Monthly newsletter', 
        'Package shipped notification',
        'HR policy updates', 
        'Conference schedule attached',
        'Holiday office hours', 
        'Payment receipt attached'
    ],
    'label': [1,1,1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0,0,0]  # 10 phishing, 10 legitimate
}

# Convert to lists of equal length
texts = train_data['text']
labels = train_data['label']

# Create and train models
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X = vectorizer.fit_transform(texts)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, labels)

# Save models
joblib.dump(model, 'phishing_model.pkl', protocol=4)
joblib.dump(vectorizer, 'vectorizer.pkl', protocol=4)

print("""
Models successfully trained and saved:
- phishing_model.pkl (Random Forest classifier)
- vectorizer.pkl (TF-IDF vectorizer)
""")

# Verify the files
try:
    m = joblib.load('phishing_model.pkl')
    v = joblib.load('vectorizer.pkl')
    print("Verification successful! Model type:", type(m))
except Exception as e:
    print("Verification failed:", str(e))
