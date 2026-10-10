import pandas as pd
import numpy as np

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def calculate_average(df):
    df['Average'] = df[['Math','Physics','Chemistry']].mean(axis=1).round(2)
    return df

def calculate_grade(avg):
    if avg >= 90:
        return 'A+'
    elif avg >= 80:
        return 'A'
    elif avg >= 70:
        return 'B'
    elif avg >= 60:
        return 'C'
    else:
        return 'D'

def add_result_columns(df):
    df['Grade'] = df['Average'].apply(calculate_grade)
    df['Status'] = np.where(df['Average'] >= 60, 'Pass', 'Fail')
    return df

def get_topper(df):
    return df.loc[df['Average'].idxmax()]

def subject_wise_avg(df):
    return df[['Math','Physics','Chemistry']].mean().round(2)