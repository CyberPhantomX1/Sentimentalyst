import matplotlib.pyplot as plt
import seaborn as sns

def visualize_sentiment_distribution(sentiments):
    """Visualize sentiment distribution."""
    sns.countplot(sentiments)
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title('Sentiment Distribution')
    plt.show()
