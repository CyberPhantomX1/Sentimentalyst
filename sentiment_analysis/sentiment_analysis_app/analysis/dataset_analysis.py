import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from gui.gui import visualize_sentiment_distribution
from model_training.model_training import train_sentiment_model
from data_preprocessing.data_preprocessing import preprocess_data

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

            dataset['text'] = dataset['text'].apply(preprocess_data)
            X = dataset['text']
            y = dataset['airline_sentiment']
            model = train_sentiment_model(X, y)
            predictions = model.predict(X)
            visualize_sentiment_distribution(predictions)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')
