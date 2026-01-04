import pandas as pd

def load_and_prepare_data(csv_path):
    df = pd.read_csv("train.csv")

    # Create binary labels: 1 = Match, 0 = No Match
    df['label'] = df['Match Percentage'].apply(lambda x: 1 if x >= 50 else 0)

    return df[['CandidateID', 'label']]
