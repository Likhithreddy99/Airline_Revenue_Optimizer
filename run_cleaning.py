import pandas as pd
import os

df = pd.read_csv('data/enhanced_airline_dataset.csv')
print("Original shape:", df.shape)

q_high = df['price'].quantile(0.99)
df_clean = df[(df['price'] > 0) & (df['price'] <= q_high)].copy()

df_clean.rename(columns={'price': 'standard_price'}, inplace=True)

required_columns = [
    'flight', 'source_city', 'destination_city', 'days_left', 
    'seats_remaining', 'standard_price', 'passenger_demand', 
    'operating_cost', 'occupancy_status', 'load_factor', 
    'is_holiday', 'is_weekend', 'season', 'flight_type', 'class'
]

df_final = df_clean[required_columns].copy()

os.makedirs('dataset/raw', exist_ok=True)
df_final.to_csv('dataset/raw/Flightprices.csv', index=False)
print("Saved to dataset/raw/Flightprices.csv with shape:", df_final.shape)
