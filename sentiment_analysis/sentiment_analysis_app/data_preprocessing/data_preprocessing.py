import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def preprocess_data(text):
    """Preprocess the text data."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join([word for word in text.split() if word not in ENGLISH_STOP_WORDS])
    return text
