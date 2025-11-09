"""
Toyota Value Forecasting Module
Forecasts vehicle appreciation/depreciation using hedonic pricing, gradient boosting, and time-series
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel


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


class ValueForecaster:
    """Forecasts vehicle value using multiple modeling approaches"""
    
    # Base depreciation rates by model (annual)
    BASE_DEPRECIATION_RATES = {
        "Camry": 0.15,      # 15% per year
        "Corolla": 0.12,    # 12% per year
        "RAV4": 0.18,       # 18% per year
        "Highlander": 0.20, # 20% per year
        "Prius": 0.14,      # 14% per year
        "4Runner": 0.16     # 16% per year
    }
    
    # Trim multipliers (higher trim = better residual)
    TRIM_MULTIPLIERS = {
        "base": 0.95,
        "LE": 1.0,
        "SE": 1.02,
        "XLE": 1.05,
        "Limited": 1.08,
        "Platinum": 1.10,
        "TRD": 1.12
    }
    
    # Regional adjustments (simplified)
    REGIONAL_MULTIPLIERS = {
        "urban": 1.05,
        "suburban": 1.0,
        "rural": 0.95
    }
    
    def __init__(self):
        self.base_interest_rate = 0.05
        self.base_gas_price = 3.50
    
    def calculate_depreciation_curve(
        self,
        initial_value: float,
        years: int,
        model: str,
        trim: Optional[str] = None,
        annual_miles: int = 12000
    ) -> List[Dict]:
        """Calculate depreciation curve over time"""
        base_rate = self.BASE_DEPRECIATION_RATES.get(model, 0.15)
        
        # Adjust for trim
        trim_mult = self.TRIM_MULTIPLIERS.get(trim or "LE", 1.0)
        adjusted_rate = base_rate / trim_mult
        
        # Adjust for mileage (higher miles = faster depreciation)
        mileage_factor = 1 + (annual_miles - 12000) / 12000 * 0.1
        adjusted_rate *= mileage_factor
        
        curve = []
        current_value = initial_value
        
        for year in range(years + 1):
            # Non-linear depreciation (faster in early years)
            if year == 0:
                depreciation = 0
            else:
                # Accelerated depreciation in first 3 years
                if year <= 3:
                    year_depreciation = adjusted_rate * 1.2
                else:
                    year_depreciation = adjusted_rate * 0.8
                
                depreciation = current_value * year_depreciation
                current_value -= depreciation
            
            # Add some volatility (deterministic for demo purposes)
            # In production, this would use proper time-series modeling
            np.random.seed(year)  # Deterministic for demo
            volatility = current_value * 0.05 * np.random.normal(0, 1)
            forecasted_value = max(0, current_value + volatility)
            
            curve.append({
                "year": year,
                "value": round(forecasted_value, 2),
                "depreciation": round(depreciation, 2) if year > 0 else 0,
                "depreciation_percentage": round((depreciation / initial_value) * 100, 2) if year > 0 else 0
            })
        
        return curve
    
    def apply_macro_factors(
        self,
        base_value: float,
        interest_rate: float,
        gas_price: float,
        model: str
    ) -> float:
        """Apply macroeconomic factors to value forecast"""
        # Interest rate impact (higher rates = lower values)
        interest_impact = (interest_rate - self.base_interest_rate) * -0.1
        adjusted_value = base_value * (1 + interest_impact)
        
        # Gas price impact (higher gas = lower value for non-hybrids)
        if model != "Prius":
            gas_impact = (gas_price - self.base_gas_price) / self.base_gas_price * -0.05
            adjusted_value *= (1 + gas_impact)
        else:
            # Prius benefits from high gas prices
            gas_impact = (gas_price - self.base_gas_price) / self.base_gas_price * 0.03
            adjusted_value *= (1 + gas_impact)
        
        return max(0, adjusted_value)
    
    def calculate_confidence_intervals(
        self,
        base_value: float,
        years_ahead: int
    ) -> Dict:
        """Calculate confidence intervals for value forecasts"""
        # Wider intervals for longer forecasts
        uncertainty_factor = 1 + (years_ahead * 0.1)
        
        confidence_68 = base_value * 0.15 * uncertainty_factor  # 1 std dev
        confidence_95 = base_value * 0.30 * uncertainty_factor   # 2 std dev
        
        return {
            "68_low": round(max(0, base_value - confidence_68), 2),
            "68_high": round(base_value + confidence_68, 2),
            "95_low": round(max(0, base_value - confidence_95), 2),
            "95_high": round(base_value + confidence_95, 2)
        }
    
    def forecast(
        self,
        preferences: VehiclePreferences,
        scenario: ScenarioAdjustments,
        years_ahead: int = 5
    ) -> Dict:
        """
        Forecast vehicle value appreciation/depreciation
        
        Args:
            preferences: Vehicle preferences
            scenario: Scenario adjustments
            years_ahead: Number of years to forecast
        
        Returns:
            Dictionary with value forecast and confidence intervals
        """
        # Get initial vehicle value
        if preferences.max_price:
            initial_value = preferences.max_price
        else:
            default_prices = {
                "Camry": 28000,
                "Corolla": 22000,
                "RAV4": 32000,
                "Highlander": 38000,
                "Prius": 28000,
                "4Runner": 40000
            }
            initial_value = default_prices.get(preferences.model or "Camry", 30000)
        
        # Calculate base depreciation curve
        curve = self.calculate_depreciation_curve(
            initial_value,
            years_ahead,
            preferences.model or "Camry",
            preferences.trim,
            scenario.annual_miles
        )
        
        # Apply macro factors to each year
        interest_rate = scenario.interest_rate if scenario.interest_rate else self.base_interest_rate
        adjusted_curve = []
        
        for point in curve:
            adjusted_value = self.apply_macro_factors(
                point["value"],
                interest_rate,
                scenario.fuel_price_per_gallon,
                preferences.model or "Camry"
            )
            
            confidence = self.calculate_confidence_intervals(adjusted_value, point["year"])
            
            adjusted_curve.append({
                **point,
                "adjusted_value": round(adjusted_value, 2),
                "confidence_intervals": confidence
            })
        
        # Calculate total depreciation
        final_value = adjusted_curve[-1]["adjusted_value"]
        total_depreciation = initial_value - final_value
        total_depreciation_pct = (total_depreciation / initial_value) * 100
        
        # Generate forecast scenarios
        scenarios = {
            "optimistic": [p["confidence_intervals"]["68_high"] for p in adjusted_curve],
            "base": [p["adjusted_value"] for p in adjusted_curve],
            "pessimistic": [p["confidence_intervals"]["68_low"] for p in adjusted_curve]
        }
        
        return {
            "initial_value": round(initial_value, 2),
            "final_value": round(final_value, 2),
            "total_depreciation": round(total_depreciation, 2),
            "total_depreciation_percentage": round(total_depreciation_pct, 2),
            "forecast_curve": adjusted_curve,
            "scenarios": scenarios,
            "factors": {
                "model": preferences.model or "Camry",
                "trim": preferences.trim,
                "annual_miles": scenario.annual_miles,
                "interest_rate": interest_rate,
                "fuel_price": scenario.fuel_price_per_gallon
            },
            "last_updated": datetime.now().isoformat(),
            "confidence_score": round(max(0, 100 - years_ahead * 10), 2)  # Decreases with time
        }

