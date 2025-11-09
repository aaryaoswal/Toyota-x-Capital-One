# Toyota x Capital One - Project Summary

## Overview
A comprehensive web application that helps users find their dream Toyota vehicles by analyzing affordability, forecasting value appreciation/depreciation, and providing personalized recommendations based on financial profiles.

## Key Features Implemented

### 1. Financial Profile Collection ✅
- Credit score input (300-850)
- Annual income and salary tracking
- Monthly budget setting
- Lease term selection (12-72 months)
- Employment subsidies tracking
- Transportation subsidy tracking

### 2. Salary & Net Pay Estimation ✅
- Real-time salary data processing
- Conservative net pay calculation with volatility
- Tax breakdown (federal, state, FICA)
- Confidence intervals (95% CI)
- Monthly and annual projections

### 3. Monthly Car Cost Cap Calculator ✅
- **Payment Calculation**: Based on APR, credit score, vehicle price, and term
- **Insurance Estimation**: Credit-score based multipliers
- **Fuel Cost**: Model-specific MPG calculations
- **Maintenance**: Percentage-based annual estimates
- **Taxes & Fees**: Sales tax, registration, inspection
- **Total Monthly Cost**: Comprehensive breakdown
- **Affordability Check**: Budget alignment and recommended maximums

### 4. Toyota Value Forecasting ✅
- **5-Year Forecasts**: Depreciation/appreciation curves
- **Model-Specific Rates**: Different depreciation by vehicle model
- **Trim Adjustments**: Higher trims retain value better
- **Mileage Factors**: Higher mileage = faster depreciation
- **Macro Factors**:
  - Interest rate impacts
  - Gas price effects (hybrid vs. gas)
- **Confidence Intervals**: 68% and 95% ranges
- **Multiple Scenarios**: Optimistic, base, pessimistic

### 5. Affordability Index ✅
Comprehensive scoring system (0-100) based on:
- **Debt-to-Income Ratio** (30% weight): Ideal 15-20%
- **Credit Score** (25% weight): 750+ = excellent
- **Budget Alignment** (20% weight): Within budget check
- **Income Stability** (15% weight): Base salary reliability
- **Term Appropriateness** (10% weight): 36-48 months ideal

Rating categories:
- Excellent (90+): Highly recommended
- Good (75-89): Recommended with minor adjustments
- Fair (60-74): Consider reducing price/down payment
- Poor (40-59): Not recommended
- Very Poor (<40): Strongly not recommended

### 6. Personalized Recommendations ✅
- **APR Matching**: Credit-score based rate calculation
- **Personal Percentage Match**: 
  - Budget alignment (50 points)
  - Income match (30 points)
  - APR match (20 points)
- **Reliability Scoring**: Based on lease term and base reliability
- **Overall Scoring**: Weighted combination of:
  - Personal match (50%)
  - Reliability (30%)
  - Affordability (20%)
- **Top 10 Recommendations**: Ranked by overall score

### 7. Interactive Visualizations ✅
- **Value Forecast Chart**: 
  - Base forecast line
  - Optimistic scenario (68% CI upper)
  - Pessimistic scenario (68% CI lower)
  - Factor toggles (interest rate, fuel price, annual miles, depreciation)
- **Component Score Bars**: Visual breakdown of affordability index
- **Cost Breakdown**: Detailed monthly expense visualization

### 8. Data Processing & Compliance ✅
- **Data Ingestion Pipeline**: Structured for licensed data sources
- **Source Labeling**: Clear identification of data types
- **Refresh Cadence**: Daily/weekly tracking
- **Last Updated Timestamps**: Transparency in data freshness
- **Disclaimers**: Clear labeling of estimates vs. actuals

### 9. Backtesting Framework ✅
- **Cohort Creation**: Historical vehicle data tracking
- **Synthetic Data Generation**: For demo purposes
- **Model Performance Metrics**:
  - Mean Absolute Error (MAE)
  - Mean Absolute Percentage Error (MAPE)
  - Root Mean Squared Error (RMSE)
- **Batch Backtesting**: Multiple models simultaneously

## Technical Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **Modules**:
  - `salary_estimator.py`: Net pay and volatility calculations
  - `cost_calculator.py`: Comprehensive monthly cost breakdown
  - `value_forecaster.py`: Depreciation/appreciation forecasting
  - `affordability_index.py`: Scoring algorithm
  - `recommendation_engine.py`: Personalized recommendations
- **Data Processing**:
  - `data_ingestion.py`: Data pipeline structure
  - `backtesting.py`: Model validation framework

### Frontend (React)
- **Framework**: React 18 with functional components
- **Visualization**: Recharts for interactive charts
- **Components**:
  - Financial profile form
  - Vehicle preferences form
  - Scenario adjustments
  - Affordability index display
  - Results dashboard
  - Value forecast chart with factor toggles
  - Recommendations list
  - Data source information

### API Endpoints
- `POST /api/estimate-salary`: Salary and net pay estimation
- `POST /api/calculate-monthly-cost`: Total monthly cost calculation
- `POST /api/forecast-value`: Value forecasting
- `POST /api/affordability-index`: Affordability scoring
- `POST /api/recommendations`: Personalized recommendations
- `GET /api/toyota-models`: Available Toyota models and trims
- `GET /api/data-sources`: Data source information and compliance

## Methodology

### Value Forecasting
- **Hedonic Pricing**: Model, trim, mileage factors
- **Time-Series Components**: Depreciation curves over time
- **Gradient Boosting Ready**: Structure for ML model integration
- **Macro Factors**: Interest rates, gas prices
- **Confidence Intervals**: Statistical ranges, not exact numbers

### Affordability Calculation
- **Conservative Estimates**: One standard deviation below mean
- **Volatility Modeling**: Income variability consideration
- **Multi-Factor Scoring**: Weighted component system
- **Guardrails**: 20% of income rule, budget constraints

## Compliance & Transparency

### Data Sources
- **Licensed Sources**: Structured for integration with real APIs
- **Public APIs**: Interest rates, gas prices
- **User Input**: Salary, financial profile
- **Refresh Cadence**: Clearly labeled (daily/weekly)
- **Last Updated**: Timestamps on all data

### Disclaimers
- All estimates are projections
- Actual values may vary
- Based on available data and models
- Confidence scores decrease over time

## Future Enhancements (Production Ready)

1. **Real Data Integration**:
   - Connect to licensed salary data APIs
   - Integrate with vehicle pricing APIs (KBB, NADA)
   - Real-time interest rate feeds
   - Gas price APIs by region

2. **Advanced ML Models**:
   - Gradient boosting for value forecasting
   - Time-series models (ARIMA, LSTM)
   - Ensemble methods for better accuracy

3. **User Features**:
   - Save profiles and scenarios
   - Compare multiple vehicles
   - Share recommendations
   - Email reports

4. **Mobile App**:
   - React Native version
   - Push notifications for price changes
   - Barcode scanning for VIN lookup

## Setup & Running

See `README.md` for detailed setup instructions.

Quick start:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

Or use the startup scripts:
- `./start.sh` (Mac/Linux)
- `start.bat` (Windows)

## Demo Notes

- All data sources are simulated for demo purposes
- Pricing data is based on 2024 MSRP estimates
- Tax calculations use simplified federal brackets
- Forecasts use deterministic models for consistency
- In production, would integrate with real licensed data sources

## Team & Credits

Developed for the Toyota x Capital One Hackathon - "The Best Financial Hack" track.

