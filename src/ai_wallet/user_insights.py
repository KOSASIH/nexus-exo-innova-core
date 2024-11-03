# src/ai_wallet/user_insights.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

class UserInsights:
    def __init__(self, transaction_history):
        self.transaction_history = pd.DataFrame(transaction_history)
        self.transaction_history['date'] = pd.to_datetime(self.transaction_history['date'])

    def get_spending_summary(self):
        summary = self.transaction_history.groupby('category')['amount'].sum().reset_index()
        summary.columns = ['Category', 'Total Spent']
        return summary

    def get_transaction_frequency(self):
        frequency = self.transaction_history['date'].dt.date.value_counts().reset_index()
        frequency.columns = ['Date', 'Frequency']
        return frequency

    def recommend_budget(self):
        average_spending = self.transaction_history['amount'].mean()
        return {
            'recommended_budget': average_spending * 1.2,  # 20% more than average spending
            'average_spending': average_spending
        }

    def visualize_spending_trends(self):
        plt.figure(figsize=(12, 6))
        spending_trends = self.transaction_history.groupby(self.transaction_history['date'].dt.to_period('M'))['amount'].sum()
        spending_trends.plot(kind='line', marker='o')
        plt.title('Monthly Spending Trends')
        plt.xlabel('Month')
        plt.ylabel('Total Spending')
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def get_category_breakdown(self):
        category_breakdown = self.transaction_history.groupby('category')['amount'].sum().reset_index()
        category_breakdown.columns = ['Category', 'Total Spent']
        return category_breakdown

    def detect_unusual_spending(self, threshold=2):
        # Calculate the mean and standard deviation of spending
        mean = self.transaction_history['amount'].mean()
        std_dev = self.transaction_history['amount'].std()
        unusual_spending = self.transaction_history[
            (self.transaction_history['amount'] > mean + threshold * std_dev) |
            (self.transaction_history['amount'] < mean - threshold * std_dev)
        ]
        return unusual_spending

    def send_alerts(self, unusual_spending):
        if not unusual_spending.empty:
            for index, row in unusual_spending.iterrows():
                print(f"Alert: Unusual spending detected - {row['amount']} on {row['date']} in category {row['category']}")

    def segment_users(self):
        # Example segmentation based on spending habits
        self.transaction_history['spending_category'] = pd.cut(
            self.transaction_history['amount'],
            bins=[0, 50, 100, 500, 1000, np.inf],
            labels=['Low', 'Medium', 'High', 'Very High', 'Extreme']
        )
        return self.transaction_history['spending_category'].value_counts()

    def get_insights(self):
        insights = {
            'spending_summary': self.get_spending_summary(),
            'transaction_frequency': self.get_transaction_frequency(),
            'recommended_budget': self.recommend_budget(),
            'category_breakdown': self.get_category_breakdown(),
            'unusual_spending': self.detect_unusual_spending(),
            'user_segments': self.segment_users()
        }
        return insights
