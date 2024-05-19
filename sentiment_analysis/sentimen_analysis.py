import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import tweepy
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from wordcloud import WordCloud
from transformers import BertTokenizer, BertForSequenceClassification
import torch

class SentimentAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sentiment Analysis')
        self.geometry('800x600')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.dataset_analysis_tab = DatasetAnalysis(self.notebook)
        self.notebook.add(self.dataset_analysis_tab, text='Analysis from Dataset')

        self.realtime_analysis_tab = RealtimeAnalysis(self.notebook)
        self.notebook.add(self.realtime_analysis_tab, text='Real-time Analysis')

class DatasetAnalysis(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.file_path_label = tk.Label(self, text='Select dataset file:')
        self.file_path_entry = tk.Entry(self, width=50)

        self.browse_button = tk.Button(self, text='Browse', command=self.browse_button_clicked)

        self.analyze_button = tk.Button(self, text='Analyze', command=self.analyze_button_clicked)

        self.file_path_label.grid(row=0, column=0, sticky='w')
        self.file_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)
        self.analyze_button.grid(row=1, columnspan=3, pady=10)

    def browse_button_clicked(self):
        """Callback function for the Browse button click."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def preprocess_data(self, text):
        """Preprocess the text data."""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join([word for word in text.split() if word not in ENGLISH_STOP_WORDS])
        return text

    def train_sentiment_model(self, X, y):
        """Train a sentiment analysis model."""
        pipeline = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('classifier', SVC(kernel='linear'))
        ])
        pipeline.fit(X, y)
        return pipeline

    def analyze_tweets_from_dataset(self, dataset):
        """Perform sentiment analysis on tweets from a dataset."""
        if 'text' not in dataset.columns:
            raise ValueError("Dataset does not contain 'text' column.")
        if 'airline_sentiment' not in dataset.columns:
            raise ValueError("Dataset does not contain 'airline_sentiment' column.")
        dataset['text'] = dataset['text'].apply(self.preprocess_data)
        X = dataset['text']
        y = dataset['airline_sentiment']
        model = self.train_sentiment_model(X, y)
        predictions = model.predict(X)
        return predictions

    def visualize_sentiment_distribution(self, sentiments):
        """Visualize sentiment distribution."""
        sns.countplot(sentiments)
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.title('Sentiment Distribution')
        plt.show()

    def analyze_button_clicked(self):
        """Callback function for the Analyze button click."""
        file_path = self.file_path_entry.get()

        if not file_path:
            messagebox.showwarning('Warning', 'Please select a dataset file.')
            return

        try:
            for encoding_type in ['utf-8', 'latin1', 'iso-8859-1', 'utf-16', 'utf-32']:
                try:
                    dataset = pd.read_csv(file_path, encoding=encoding_type)
                    break
                except UnicodeDecodeError:
                    continue

            sentiments = self.analyze_tweets_from_dataset(dataset)
            self.visualize_sentiment_distribution(sentiments)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')

class RealtimeAnalysis(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.keyword_label = tk.Label(self, text='Enter the keyword to search tweets:')
        self.keyword_entry = tk.Entry(self, width=50)

        self.num_tweets_label = tk.Label(self, text='Enter the number of tweets to fetch:')
        self.num_tweets_entry = tk.Entry(self, width=10)

        self.analyze_button = tk.Button(self, text='Analyze', command=self.analyze_button_clicked)

        self.keyword_label.grid(row=0, column=0, sticky='w')
        self.keyword_entry.grid(row=0, column=1, padx=5, pady=5)
        self.num_tweets_label.grid(row=1, column=0, sticky='w')
        self.num_tweets_entry.grid(row=1, column=1, padx=5, pady=5)
        self.analyze_button.grid(row=2, columnspan=2, pady=10)

    def analyze_button_clicked(self):
        """Callback function for the Analyze button click."""
        keyword = self.keyword_entry.get()
        num_tweets = self.num_tweets_entry.get()

        if not keyword:
            messagebox.showwarning('Warning', 'Please enter a keyword.')
            return

        if not num_tweets.isdigit():
            messagebox.showwarning('Warning', 'Please enter a valid number of tweets.')
            return

        num_tweets = int(num_tweets)
        
        # Perform real-time analysis using Twitter and YouTube APIs
        twitter_analysis(keyword, num_tweets)
        youtube_analysis(keyword)

def twitter_analysis(keyword, num_tweets):
    # Twitter API authentication
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    access_token = 'YOUR_ACCESS_TOKEN'
    access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Fetch tweets
    tweets = api.search(q=keyword, count=num_tweets)

    # Perform sentiment analysis on tweets and display results
    for tweet in tweets:
        # Perform sentiment analysis on each tweet
        # Display the tweet and its sentiment
        pass

def youtube_analysis(keyword):
    # YouTube API key
    api_key = 'YOUR_YOUTUBE_API_KEY'

    # Build a YouTube client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Search for videos with the given keyword
    request = youtube.search().list(
        q=keyword,
        part='snippet',
        type='video',
        maxResults=10
