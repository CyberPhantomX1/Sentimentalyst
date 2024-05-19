from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

def train_sentiment_model(X, y):
    """Train a sentiment analysis model."""
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('classifier', SVC(kernel='linear'))
    ])
    pipeline.fit(X, y)
    return pipeline
