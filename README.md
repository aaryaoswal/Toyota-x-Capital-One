# Toyota x Capital One - Vehicle Affordability & Value Forecasting Platform

A comprehensive web application that helps users find their dream Toyota vehicles by analyzing affordability, forecasting value appreciation/depreciation, and providing personalized recommendations.

## Features

- **Salary & Net Pay Estimation**: Real-time salary data ingestion with volatility calculations
- **Monthly Car Cost Cap Calculator**: Comprehensive cost analysis including payment, insurance, fuel, maintenance, taxes, and fees
- **Toyota Value Forecasting**: Advanced models using hedonic pricing, gradient boosting, and time-series analysis
- **Affordability Index**: Personalized affordability scoring based on financial profile
- **Interactive Visualizations**: Depreciation/appreciation graphs with adjustable factors
- **Personalized Recommendations**: APR matching, percentage match, and reliability scoring

## Project Structure

```
Toyota-x-Capital-One/
├── backend/                    # FastAPI backend server
│   ├── main.py                 # API endpoints and routing
│   ├── modules/                 # Core business logic modules
│   │   ├── salary_estimator.py      # Net pay & volatility
│   │   ├── cost_calculator.py       # Monthly cost breakdown
│   │   ├── value_forecaster.py      # Depreciation forecasting
│   │   ├── affordability_index.py   # Affordability scoring
│   │   └── recommendation_engine.py # Personalized recommendations
│   └── requirements.txt
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── App.js              # Main application component
│   │   └── components/         # React components
│   │       ├── FinancialProfileForm.js
│   │       ├── VehiclePreferencesForm.js
│   │       ├── ScenarioAdjustments.js
│   │       ├── AffordabilityIndex.js
│   │       ├── ResultsDashboard.js
│   │       ├── ValueForecastChart.js
│   │       ├── Recommendations.js
│   │       └── DataSourceInfo.js
│   └── package.json
├── data_processing/             # Data ingestion and processing
│   ├── data_ingestion.py        # Data pipeline structure
│   └── backtesting.py           # Model validation framework
├── requirements.txt             # Python dependencies
├── start.sh                     # Startup script (Mac/Linux)
├── start.bat                    # Startup script (Windows)
├── README.md                    # This file
└── PROJECT_SUMMARY.md           # Detailed project documentation
```

## Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## API Documentation

Once the backend server is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Features Overview

### Financial Profile Collection
- Credit score input
- Annual income and salary
- Monthly budget
- Lease term selection
- Employment and transportation subsidies

### Affordability Analysis
- **Affordability Index**: Comprehensive scoring based on:
  - Debt-to-income ratio
  - Credit score
  - Budget alignment
  - Income stability
  - Term appropriateness

### Cost Calculator
- Monthly payment calculation
- Insurance estimation
- Fuel cost projection
- Maintenance estimates
- Taxes and fees
- Total monthly cost cap

### Value Forecasting
- 5-year depreciation/appreciation curves
- Confidence intervals (68% and 95%)
- Scenario adjustments:
  - Interest rates
  - Fuel prices
  - Annual mileage
- Interactive visualization with factor toggles

### Personalized Recommendations
- APR matching based on credit score
- Personal percentage match calculation
- Reliability scoring based on lease term
- Top 10 vehicle recommendations ranked by overall score

### Compliance & Transparency
- Data source labeling
- Refresh cadence information
- Clear assumptions display
- Disclaimer for estimates

## License

This project is developed for the Toyota x Capital One Hackathon.

