import joblib
import pandas as pd

# Load the trained model
model = joblib.load("trained_model\model.pkl")

# Sample input: Match Percentage (you can replace this with dynamic input)
sample_data = pd.DataFrame({
    "Match Percentage": [65, 40, 80]  # You can change or extend this list
})

# Predict using the model
predictions = model.predict(sample_data)

# Display results
for i, pred in enumerate(predictions):
    status = "Suitable" if pred == 1 else "Not Suitable"
    print(f"Resume {i + 1} (Match: {sample_data.iloc[i]['Match Percentage']}%) → {status}")


