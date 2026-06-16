import pandas as pd
import numpy as np

print("Loading dataset...")
df = pd.read_csv('data/enhanced_airline_dataset.csv')

print("Generating class-sensitive price-elastic demand...")
np.random.seed(42)
noise = np.random.normal(0, 10, len(df))

df['passenger_demand'] = 0
is_econ = df['class'] == 'Economy'
is_bus = df['class'] == 'Business'

# Economy: higher base demand, very sensitive to price (falls off above 15k)
df.loc[is_econ, 'passenger_demand'] = (260 - 0.015 * df.loc[is_econ, 'price'] + noise[is_econ]).clip(30, df.loc[is_econ, 'seat_capacity']).astype(int)

# Business: lower base demand, less sensitive to price (ranges up to 100k)
df.loc[is_bus, 'passenger_demand'] = (180 - 0.0015 * df.loc[is_bus, 'price'] + noise[is_bus]).clip(20, df.loc[is_bus, 'seat_capacity']).astype(int)

# Update dependent columns
df['seats_remaining'] = df['seat_capacity'] - df['passenger_demand']
df['load_factor'] = (df['passenger_demand'] / df['seat_capacity'] * 100).round(2)
df['revenue'] = (df['price'] * df['passenger_demand']).round(2)

# Cost and profit
cost_ratio = np.random.uniform(0.50, 0.75, len(df))
df['operating_cost'] = (df['revenue'] * cost_ratio).round(2)
df['profit'] = (df['revenue'] - df['operating_cost']).round(2)
df['profit_margin'] = (df['profit'] / df['revenue'] * 100).round(2)

# occupancy status
cond_occupancy = [
    df['load_factor'] < 70,
    (df['load_factor'] >= 70) & (df['load_factor'] < 90),
    df['load_factor'] >= 90
]
choices_occupancy = ['Low Occupancy', 'Normal Occupancy', 'Near Full']
df['occupancy_status'] = np.select(cond_occupancy, choices_occupancy, default='Normal Occupancy')

# demand level
cond_demand = [
    df['passenger_demand'] < 100,
    df['passenger_demand'] < 170,
    df['passenger_demand'] >= 170
]
choices_demand = ['Low', 'Medium', 'High']
df['demand_level'] = np.select(cond_demand, choices_demand, default='Medium')

# demand elasticity
df['demand_elasticity'] = (df['passenger_demand'] / df['price']).round(4)

print("Saving updated dataset...")
df.to_csv('data/enhanced_airline_dataset.csv', index=False)
print("Saved successfully!")
