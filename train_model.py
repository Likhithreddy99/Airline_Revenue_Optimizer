import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib

def main():
    print("Loading dataset...")
    try:
        df = pd.read_csv('dataset/raw/Flightprices.csv')
    except FileNotFoundError:
        print("Error: dataset/raw/Flightprices.csv not found.")
        return

    print("Preprocessing data...")
    features = ['days_left', 'is_holiday', 'is_weekend', 'standard_price', 'season', 'flight_type', 'class']
    target = 'passenger_demand'

    X = df[features].copy()
    y = df[target].copy()

    # Handle categorical encoding (One-Hot) for season and flight_type
    X = pd.get_dummies(X, columns=['season', 'flight_type', 'class'], drop_first=False)
    
    # Keep track of feature columns to ensure consistency during inference
    feature_columns = list(X.columns)

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training XGBoost Regressor...")
    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    print("Evaluating model...")
    score = model.score(X_test, y_test)
    print(f"R^2 Score on test set: {score:.4f}")

    print("Saving model and features...")
    # Export the trained model and feature columns using joblib
    joblib.dump({
        'model': model,
        'feature_columns': feature_columns
    }, 'model.joblib')
    
    print("Training complete! Model saved to model.joblib.")

if __name__ == "__main__":
    main()
