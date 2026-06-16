import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Airline Revenue Optimizer - Data Cleaning & EDA\n",
                "This notebook performs exploratory data analysis (EDA) and data cleaning for the Airline Revenue Optimizer project.\n",
                "We handle missing values, anomalies (like bizarre prices), and prepare the dataset for the XGBoost model."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "\n",
                "# Set plot style\n",
                "sns.set(style='darkgrid')\n",
                "plt.rcParams['figure.figsize'] = (10, 6)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Load Dataset\n",
                "Load the enhanced airline dataset."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df = pd.read_csv('data/enhanced_airline_dataset.csv')\n",
                "print(f\"Dataset shape: {df.shape}\")\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Exploratory Data Analysis (EDA)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Basic statistics\n",
                "df.describe()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Check for missing values\n",
                "df.isnull().sum()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Distribution of standard_price (which we might just call 'price')\n",
                "sns.histplot(df['price'], bins=50, kde=True)\n",
                "plt.title('Distribution of Flight Prices')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Data Cleaning\n",
                "Remove bizarre prices (anomalies). We will remove prices that are <= 0, and extreme outliers (e.g., above the 99th percentile or unrealistic values)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Identify bizarre prices\n",
                "print(\"Number of negative or zero prices:\", (df['price'] <= 0).sum())\n",
                "q_high = df['price'].quantile(0.99)\n",
                "print(f\"99th percentile price: {q_high}\")\n",
                "\n",
                "# Filter out anomalies (price <= 0 and price > 99th percentile)\n",
                "df_clean = df[(df['price'] > 0) & (df['price'] <= q_high)].copy()\n",
                "print(f\"Cleaned dataset shape: {df_clean.shape}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Feature Selection & Renaming\n",
                "Prepare features for the XGBoost model. We need: `days_left`, `seats_remaining`, `standard_price` (mapped from `price`), `passenger_demand`, `is_holiday`, `is_weekend`, `season`, `flight_type`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Rename price to standard_price to match user requirements\n",
                "df_clean.rename(columns={'price': 'standard_price'}, inplace=True)\n",
                "\n",
                "required_columns = [\n",
                "    'flight', 'source_city', 'destination_city', 'days_left', \n",
                "    'seats_remaining', 'standard_price', 'passenger_demand', \n",
                "    'operating_cost', 'occupancy_status', 'load_factor', \n",
                "    'is_holiday', 'is_weekend', 'season', 'flight_type'\n",
                "]\n",
                "\n",
                "# Ensure all required columns exist\n",
                "for col in required_columns:\n",
                "    if col not in df_clean.columns:\n",
                "        print(f\"Warning: {col} is missing! Filling with defaults.\")\n",
                "        if col == 'flight_type':\n",
                "            df_clean[col] = 'Short Haul'\n",
                "        elif col == 'occupancy_status':\n",
                "            df_clean[col] = 'Normal'\n",
                "        elif col == 'load_factor':\n",
                "            df_clean[col] = 0.7\n",
                "        else:\n",
                "            df_clean[col] = 0\n",
                "\n",
                "df_final = df_clean[required_columns].copy()\n",
                "df_final.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Save Cleaned Dataset\n",
                "Save the cleaned dataset so `train_model.py` and `app.py` can use it."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "os.makedirs('dataset/raw', exist_ok=True)\n",
                "df_final.to_csv('dataset/raw/Flightprices.csv', index=False)\n",
                "print(\"Cleaned dataset saved successfully to dataset/raw/Flightprices.csv!\")"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.9.7"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open('eda.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Created eda.ipynb")
