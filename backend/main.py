from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn

from modules.salary_estimator import SalaryEstimator
from modules.cost_calculator import CostCalculator
from modules.value_forecaster import ValueForecaster
from modules.affordability_index import AffordabilityIndex
from modules.recommendation_engine import RecommendationEngine

app = FastAPI(title="Toyota Vehicle Affordability API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
salary_estimator = SalaryEstimator()
cost_calculator = CostCalculator()
value_forecaster = ValueForecaster()
affordability_index = AffordabilityIndex()
recommendation_engine = RecommendationEngine()

# Request/Response Models
class FinancialProfile(BaseModel):
    credit_score: int
    annual_income: float
    monthly_budget: float
    lease_term_months: int
    salary: float
    employment_subsidies: float = 0.0
    transportation_subsidy: float = 0.0

class VehiclePreferences(BaseModel):
    make: str = "Toyota"
    model: Optional[str] = None
    trim: Optional[str] = None
    max_price: Optional[float] = None
    preferred_fuel_type: Optional[str] = None

class ScenarioAdjustments(BaseModel):
    annual_miles: int = 12000
    fuel_price_per_gallon: float = 3.50
    internship_length_months: Optional[int] = None
    interest_rate: Optional[float] = None

@app.get("/")
async def root():
    return {"message": "Toyota Vehicle Affordability API", "version": "1.0.0"}

@app.post("/api/estimate-salary")
async def estimate_salary(profile: FinancialProfile):
    """Estimate net pay and volatility from salary data"""
    try:
        result = salary_estimator.estimate(profile.salary, profile.employment_subsidies)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/calculate-monthly-cost")
async def calculate_monthly_cost(
    profile: FinancialProfile,
    preferences: VehiclePreferences,
    scenario: ScenarioAdjustments
):
    """Calculate total monthly car cost cap"""
    try:
        result = cost_calculator.calculate_total_cost(
            profile=profile,
            preferences=preferences,
            scenario=scenario
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/forecast-value")
async def forecast_value(
    preferences: VehiclePreferences,
    scenario: ScenarioAdjustments,
    years_ahead: int = 5
):
    """Forecast vehicle value appreciation/depreciation"""
    try:
        result = value_forecaster.forecast(
            preferences=preferences,
            scenario=scenario,
            years_ahead=years_ahead
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/affordability-index")
async def get_affordability_index(
    profile: FinancialProfile,
    preferences: VehiclePreferences,
    scenario: ScenarioAdjustments
):
    """Calculate affordability index score"""
    try:
        # First calculate monthly cost to pass to affordability index
        monthly_cost_result = cost_calculator.calculate_total_cost(
            profile=profile,
            preferences=preferences,
            scenario=scenario
        )
        monthly_cost = monthly_cost_result["cost_breakdown"]["total"]
        
        result = affordability_index.calculate(
            profile=profile,
            preferences=preferences,
            scenario=scenario,
            monthly_cost=monthly_cost
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommendations")
async def get_recommendations(
    profile: FinancialProfile,
    preferences: VehiclePreferences,
    scenario: ScenarioAdjustments
):
    """Get personalized vehicle recommendations"""
    try:
        result = recommendation_engine.generate_recommendations(
            profile=profile,
            preferences=preferences,
            scenario=scenario
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/toyota-models")
async def get_toyota_models():
    """Get available Toyota models"""
    return {
        "models": [
            {"name": "Camry", "trims": ["LE", "SE", "XLE", "XSE"]},
            {"name": "Corolla", "trims": ["L", "LE", "SE", "XLE", "XSE"]},
            {"name": "RAV4", "trims": ["LE", "XLE", "XLE Premium", "Limited", "Adventure"]},
            {"name": "Highlander", "trims": ["L", "LE", "XLE", "Limited", "Platinum"]},
            {"name": "Prius", "trims": ["LE", "XLE", "Limited"]},
            {"name": "4Runner", "trims": ["SR5", "TRD Off-Road", "Limited", "TRD Pro"]},
        ]
    }

@app.get("/api/data-sources")
async def get_data_sources():
    """Get information about data sources and refresh cadence"""
    return {
        "sources": [
            {
                "name": "Salary Data",
                "type": "Licensed",
                "refresh_cadence": "Daily",
                "last_updated": "2024-01-15"
            },
            {
                "name": "Vehicle Pricing",
                "type": "Licensed",
                "refresh_cadence": "Weekly",
                "last_updated": "2024-01-14"
            },
            {
                "name": "Interest Rates",
                "type": "Public API",
                "refresh_cadence": "Daily",
                "last_updated": "2024-01-15"
            }
        ],
        "disclaimer": "All estimates are projections based on available data and models. Actual values may vary."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

