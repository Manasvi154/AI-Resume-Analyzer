import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import pickle  # for future use (if vectorizer is used)

# Load dataset
df = pd.read_csv("train.csv")

# Drop CandidateID
df = df.drop(columns=["CandidateID"])

# Create binary labels from Match Percentage
df["label"] = df["Match Percentage"].apply(lambda x: 1 if x >= 50 else 0)

import numpy as np

# Flip a few labels randomly (simulate noise)
np.random.seed(42)
flip_indices = np.random.choice(df.index, size=3, replace=False)
df.loc[flip_indices, "label"] = 1 - df.loc[flip_indices, "label"]

# Use Match Percentage as a feature
X = df[["Match Percentage"]]
y = df["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X_train, y_train)

# Predictions
y_pred = clf.predict(X_test)

# Evaluation
print("\nModel Evaluation:")
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}")
print(classification_report(y_test, y_pred))

# Save the model
os.makedirs("trained_model", exist_ok=True)
joblib.dump(clf, "trained_model/model.pkl")
print("\nModel saved to trained_model/model.pkl")

