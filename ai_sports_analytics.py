import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

# Load the dataset
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Preprocessing
def preprocess_data(data):
    # Fill missing values
    data.fillna(data.mean(), inplace=True)
    
    # Convert categorical variables to dummy variables
    data = pd.get_dummies(data, drop_first=True)
    
    return data

# Feature selection
def feature_selection(data, target_column):
    features = data.drop(columns=[target_column])
    target = data[target_column]
    return features, target

# Split the data into train and test sets
def split_data(features, target, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

# Train a linear regression model
def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Train a random forest model
def train_random_forest(X_train, y_train):
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    return model

# Evaluate model performance
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return mse

# Save the model
def save_model(model, filename):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")

# Load the model
def load_model(filename):
    model = joblib.load(filename)
    print(f"Model loaded from {filename}")
    return model

# Feature importance
def plot_feature_importance(model, feature_names):
    importance = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
    feature_importance_df = feature_importance_df.sort_values('Importance', ascending=False)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_importance_df.head(10))
    plt.title('Top 10 Feature Importances')
    plt.show()

# Main function
def main():
    file_path = 'sports_data.csv'  # Change this to your dataset path
    target_column = 'performance_score'  # Change to your target column
    data = load_data(file_path)
    
    if data is not None:
        data = preprocess_data(data)
        features, target = feature_selection(data, target_column)
        X_train, X_test, y_train, y_test = split_data(features, target)

        # Linear Regression Model
        lr_model = train_linear_regression(X_train, y_train)
        lr_mse = evaluate_model(lr_model, X_test, y_test)
        print(f'Linear Regression MSE: {lr_mse}')
        
        # Random Forest Model
        rf_model = train_random_forest(X_train, y_train)
        rf_mse = evaluate_model(rf_model, X_test, y_test)
        print(f'Random Forest MSE: {rf_mse}')

        # Save the models
        save_model(lr_model, 'linear_regression_model.pkl')
        save_model(rf_model, 'random_forest_model.pkl')

        # Feature importance
        plot_feature_importance(rf_model, features.columns)

if __name__ == "__main__":
    main()