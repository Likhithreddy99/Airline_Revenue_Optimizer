import sys
import os

# Add parent directory to path so we can import src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np

from ml_pipeline.pipeline.predictpipeline import PredictPipeline, CustomData

app = FastAPI(title="Airline Revenue Optimizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predict_pipeline = PredictPipeline()

# Try to load raw data for dashboards
try:
    df = pd.read_csv("data/enhanced_airline_dataset.csv")
    q_high = df['price'].quantile(0.99)
    df = df[(df['price'] > 0) & (df['price'] <= q_high)].copy()
    df.rename(columns={'price': 'standard_price'}, inplace=True)
except Exception as e:
    df = pd.DataFrame()

class FlightRequest(BaseModel):
    days_left: int
    seats_remaining: int
    is_holiday: bool
    is_weekend: bool
    season: str
    flight_type: str
    class_type: str = "Economy"
    operating_cost: float = 5000.0

@app.get("/")
def read_root():
    return {"message": "Airline Revenue Optimizer API is running"}

@app.post("/api/predict_optimal_price")
def predict_optimal_price(req: FlightRequest):
    try:
        # Dynamically set search range in Indian Rupees based on class and flight type
        if req.class_type == 'Economy':
            if req.flight_type == 'Short Haul':
                price_points = np.linspace(1000, 20000, 100)
            elif req.flight_type == 'Medium Haul':
                price_points = np.linspace(2000, 30000, 100)
            else:
                price_points = np.linspace(3000, 45000, 100)
        else:  # Business class
            if req.flight_type == 'Short Haul':
                price_points = np.linspace(10000, 50000, 100)
            elif req.flight_type == 'Medium Haul':
                price_points = np.linspace(15000, 80000, 100)
            else:
                price_points = np.linspace(20000, 120000, 100)

        best_price = price_points[0]
        max_profit = -float('inf')
        best_demand = 0
        best_revenue = 0

        for p in price_points:
            data = CustomData(
                days_left=req.days_left,
                standard_price=float(p),
                is_holiday=1 if req.is_holiday else 0,
                is_weekend=1 if req.is_weekend else 0,
                season=req.season,
                flight_type=req.flight_type,
                class_type=req.class_type
            )
            features_df = data.get_data_as_data_frame()
            
            pred_demand = predict_pipeline.predict(features_df)[0]
            actual_demand = max(0, min(pred_demand, req.seats_remaining))
            
            revenue = p * actual_demand
            profit = revenue - req.operating_cost
            
            if profit > max_profit:
                max_profit = profit
                best_price = p
                best_demand = actual_demand
                best_revenue = revenue

        return {
            "optimal_price": float(best_price),
            "predicted_demand": int(best_demand),
            "estimated_revenue": float(best_revenue),
            "estimated_profit": float(max_profit)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/urgency_data")
def get_urgency_data():
    if df.empty:
        raise HTTPException(status_code=404, detail="Data not available")
    
    # Sample data to avoid massive payload
    sample_df = df.sample(min(2000, len(df)))
    
    # Format for Recharts
    # We want x: days_left, y: seats_remaining, z: occupancy_status/load_factor
    data = []
    for _, row in sample_df.iterrows():
        status = row.get("occupancy_status", "Normal")
        load = row.get("load_factor", 0.7)
        category = "Safe"
        if "Low" in str(status) and row["days_left"] < 7 and load < 0.65:
            category = "Critical"
        elif "Low" in str(status) and row["days_left"] < 14:
            category = "Warning"
            
        data.append({
            "flight": str(row["flight"]),
            "days_left": float(row["days_left"]),
            "seats_remaining": float(row["seats_remaining"]),
            "status": str(status),
            "category": category,
            "load_factor": float(load)
        })
    return {"data": data}

@app.get("/api/route_profitability")
def get_route_profitability():
    if df.empty or 'profit' not in df.columns or 'revenue' not in df.columns:
        raise HTTPException(status_code=404, detail="Profit/Revenue data not available")
    
    route_agg = df.groupby(['source_city', 'destination_city']).agg(
        Total_Revenue=('revenue', 'sum'),
        Avg_Profit_Margin=('profit_margin', 'mean')
    ).reset_index()
    
    # Limit to top 20 for UI
    route_agg = route_agg.sort_values(by="Total_Revenue", ascending=False).head(20)
    
    routes = []
    for _, row in route_agg.iterrows():
        routes.append({
            "route": f"{row['source_city']} - {row['destination_city']}",
            "revenue": float(row['Total_Revenue']),
            "margin": float(row['Avg_Profit_Margin'])
        })
        
    return {"data": routes}
