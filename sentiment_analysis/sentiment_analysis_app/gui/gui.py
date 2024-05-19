import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from data_preprocessing.data_preprocessing import preprocess_data
from model_training.model_training import train_sentiment_model
from visualization.visualization import visualize_sentiment_distribution
from analysis.dataset_analysis import DatasetAnalysis
from analysis.realtime_analysis import RealtimeAnalysis

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
