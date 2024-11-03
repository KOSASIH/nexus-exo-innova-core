# src/ai_wallet/fraud_detection.py

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import joblib
import smtplib
from email.mime.text import MIMEText

class FraudDetection:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.transaction_data = pd.DataFrame(columns=['amount', 'time', 'user_id', 'is_fraud'])

    def add_transaction(self, amount, time, user_id, is_fraud):
        new_transaction = pd.DataFrame([[amount, time, user_id, is_fraud]], columns=self.transaction_data.columns)
        self.transaction_data = pd.concat([self.transaction_data, new_transaction], ignore_index=True)

    def train_model(self):
        if self.transaction_data.empty:
            print("No transaction data available for training.")
            return

        X = self.transaction_data[['amount', 'time', 'user_id']]
        y = self.transaction_data['is_fraud']

        # Feature scaling
        X_scaled = self.scaler.fit_transform(X)

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Train the model
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))

        # Save the model
        joblib.dump(self.model, 'fraud_detection_model.pkl')
        joblib.dump(self.scaler, 'scaler.pkl')

    def load_model(self):
        self.model = joblib.load('fraud_detection_model.pkl')
        self.scaler = joblib.load('scaler.pkl')

    def detect_fraud(self, transaction):
        # transaction should be a dictionary with keys: amount, time, user_id
        transaction_data = pd.DataFrame([transaction])
        transaction_data[['amount', 'time', 'user_id']] = self.scaler.transform(transaction_data[['amount', 'time', 'user_id']])
        prediction = self.model.predict(transaction_data[['amount', 'time', 'user_id']])
        return prediction[0] == 1  # 1 indicates fraud

    def notify_user(self, user_email, transaction):
        subject = "Fraud Alert"
        body = f"Suspicious transaction detected:\n\n{transaction}"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'noreply@yourwallet.com'
        msg['To'] = user_email

        # Send email
        with smtplib.SMTP('smtp.your-email-provider.com', 587) as server:
            server.starttls()
            server.login('your-email@example.com', 'your-email-password')
            server.send_message(msg)

    def report_fraud(self, transaction):
        # Placeholder for user feedback loop
        print("User  reported fraud for transaction:", transaction)
        self.add_transaction(transaction['amount'], transaction['time'], transaction['user_id'], is_fraud=1)
        self.train_model()  # Retrain the model with the new data
