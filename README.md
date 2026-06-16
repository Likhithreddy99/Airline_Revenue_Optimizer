# Airline Revenue Optimizer (ARO) ✈️📈

A premium, production-grade SaaS-style **Airline Revenue Optimizer** built with a **FastAPI backend**, a **React (Vite) frontend**, and an end-to-end **XGBoost machine learning pipeline**. The tool simulates market demand based on price, seat scarcity, booking windows, and seasonality, calculating the mathematically optimal ticket price that maximizes revenue.

---

## 🚀 Key Features

*   **Dynamic Price Optimization Tool:** Input flight parameters (Days Left, Seats Remaining, Season, Flight Type, Class, and Operating Cost) to predict demand and determine the optimal, revenue-maximizing ticket price.
*   **Detailed Revenue Analytics:** Instant breakdown of Estimated Revenue, predicted ticket sales (pax), and Estimated Net Profit (Revenue - Cost).
*   **Flight Watch Dashboard (Urgency Matrix):** A dynamic scatter plot visualizing distressed inventory across the flight network, categorizing flights into **Critical**, **Warning**, and **Safe** zones based on load factor and days to departure.
*   **Route Profitability Hub:** A clean horizontal bar chart visualizing the top 20 most profitable flight routes, with color-coded margin status.
*   **Class-Sensitive Pricing Curves:** Predicts demand curves separately for Economy and Business class, reflecting different price elasticities (Economy demand drops off rapidly above ₹15,000, whereas Business ranges up to ₹120,000).

---

## 🛠️ Technology Stack

*   **Frontend:** React (Vite), Axios, Recharts (Charts/Dashboards), Lucide React (Icons), Custom HSL Light Theme CSS.
*   **Backend:** FastAPI, Uvicorn (ASGI Server), Pydantic (Data validation).
*   **Machine Learning Core:** XGBoost Regressor (Scipy/Sklearn Pipeline), Joblib, Pandas, NumPy.

---

## 📂 Project Structure

```text
simpleairline/
├── backend/
│   ├── app/                      # Backend application code
│   ├── artifacts/                # Trained models & preprocessors
│   │   ├── model.pkl             # XGBoost model
│   │   └── preprocessor.pkl      # Scaler and Categorical encoders
│   ├── ml_pipeline/              # ML Pipeline source code
│   │   ├── components/           # Ingestion, transformation, training
│   │   └── pipeline/             # Orchestration pipelines
│   ├── main.py                   # FastAPI main entrypoint
│   └── requirements.txt          # Backend dependencies
├── data/
│   └── enhanced_airline_dataset.csv  # Enhanced training data (300k+ rows)
├── dataset/
│   └── raw/
│       └── Flightprices.csv      # Cleaned baseline data
├── frontend/
│   ├── public/                   # Static assets (custom ARO Logo)
│   ├── src/
│   │   ├── App.jsx               # Main React dashboard component
│   │   ├── index.css             # Main styling system
│   │   └── main.jsx
│   └── package.json              # Frontend dependencies
├── scratch/                      # Temporary helper scripts
├── train_model.py                # Baseline training script
├── run_cleaning.py               # Dataset ingestion cleaning script
└── README.md                     # Documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites
*   Node.js (v18+) & npm
*   Python (3.8+) & pip

### 1. Backend Setup (FastAPI & ML Core)
1.  Navigate to the project directory:
    ```bash
    cd simpleairline
    ```
2.  Install python dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```
3.  *(Optional)* Retrain the machine learning model on the updated price-elastic dataset:
    ```bash
    PYTHONPATH=backend python3 backend/ml_pipeline/pipeline/trainpipeline.py
    ```
4.  Start the FastAPI server:
    ```bash
    PYTHONPATH=backend uvicorn backend.main:app --port 8000 --reload
    ```
    The API will be available at `http://localhost:8000`.

### 2. Frontend Setup (React & Vite)
1.  Navigate to the `frontend` folder:
    ```bash
    cd frontend
    ```
2.  Install node modules:
    ```bash
    npm install
    ```
3.  Start the Vite development server:
    ```bash
    npm run dev
    ```
    The application will open automatically at `http://localhost:5173/`.

---

## 🧠 Machine Learning Details

The forecasting engine uses an **XGBoost Regressor** trained on **297,153 historical flights** to predict passenger demand.

### Feature Set
*   **Numerical Features:** `days_left`, `standard_price` (ticket price), `is_holiday`, `is_weekend`.
*   **Categorical Features:** `season` (Peak, Summer, Monsoon, Winter), `flight_type` (Short/Medium/Long Haul), `class` (Economy/Business).
*   *Note: `seats_remaining` is excluded from feature training to prevent target leakage, keeping the demand prediction independent of aircraft capacities until final booking constraints are applied.*

### Performance
*   **Model Accuracy (R² Score):** **0.8837** (88.37% variance explained).
*   **Primary Predictor:** `standard_price` (97.97% feature importance), representing highly realistic price-elastic demand response.
