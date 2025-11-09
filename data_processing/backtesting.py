"""
Backtesting Framework
Backtests value forecasting models on Toyota vehicle cohorts
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json


class BacktestingFramework:
    """Backtests forecasting models on historical Toyota vehicle data"""
    
    def __init__(self):
        # Historical data structure (in production, this would come from database)
        self.historical_cohorts = []
    
    def create_cohort(
        self,
        model: str,
        trim: str,
        purchase_date: datetime,
        purchase_price: float,
        initial_mileage: int = 0
    ) -> Dict:
        """Create a vehicle cohort for backtesting"""
        cohort = {
            "model": model,
            "trim": trim,
            "purchase_date": purchase_date.isoformat(),
            "purchase_price": purchase_price,
            "initial_mileage": initial_mileage,
            "historical_values": []
        }
        
        self.historical_cohorts.append(cohort)
        return cohort
    
    def add_historical_value(
        self,
        cohort_id: int,
        date: datetime,
        value: float,
        mileage: int,
        condition: str = "good"
    ):
        """Add historical value data point to a cohort"""
        if cohort_id < len(self.historical_cohorts):
            self.historical_cohorts[cohort_id]["historical_values"].append({
                "date": date.isoformat(),
                "value": value,
                "mileage": mileage,
                "condition": condition
            })
    
    def generate_synthetic_cohort_data(
        self,
        model: str,
        trim: str,
        purchase_price: float,
        years: int = 5
    ) -> Dict:
        """Generate synthetic historical data for backtesting"""
        purchase_date = datetime.now() - timedelta(days=years * 365)
        
        # Base depreciation rates
        depreciation_rates = {
            "Camry": 0.15,
            "Corolla": 0.12,
            "RAV4": 0.18,
            "Highlander": 0.20,
            "Prius": 0.14,
            "4Runner": 0.16
        }
        
        base_rate = depreciation_rates.get(model, 0.15)
        
        historical_values = []
        current_value = purchase_price
        current_mileage = 0
        annual_miles = 12000
        
        for year in range(years + 1):
            date = purchase_date + timedelta(days=year * 365)
            
            if year > 0:
                # Apply depreciation
                year_depreciation = current_value * base_rate * (1.2 if year <= 3 else 0.8)
                current_value -= year_depreciation
                current_mileage += annual_miles
                
                # Add some volatility
                volatility = current_value * 0.05 * np.random.normal(0, 1)
                current_value = max(0, current_value + volatility)
            
            historical_values.append({
                "date": date.isoformat(),
                "value": round(current_value, 2),
                "mileage": current_mileage,
                "condition": "good" if year < 3 else "fair"
            })
        
        return {
            "model": model,
            "trim": trim,
            "purchase_date": purchase_date.isoformat(),
            "purchase_price": purchase_price,
            "historical_values": historical_values
        }
    
    def backtest_forecast(
        self,
        forecast_model,
        cohort_data: Dict,
        forecast_start_date: datetime
    ) -> Dict:
        """Backtest a forecast model against historical data"""
        # Filter historical data after forecast start
        historical_after_forecast = [
            v for v in cohort_data["historical_values"]
            if datetime.fromisoformat(v["date"]) >= forecast_start_date
        ]
        
        if not historical_after_forecast:
            return {
                "error": "Insufficient historical data for backtesting"
            }
        
        # Generate forecast (this would use the actual forecast model)
        # For now, we'll simulate
        forecast_values = []
        actual_values = []
        
        for i, historical_point in enumerate(historical_after_forecast):
            # In production, this would use the actual forecast model
            # For now, we'll use a simple linear extrapolation
            if i == 0:
                forecast_value = historical_point["value"]
            else:
                # Simple forecast (would be replaced with actual model)
                prev_forecast = forecast_values[i - 1]
                prev_actual = actual_values[i - 1]
                depreciation_rate = 0.15 / 12  # Monthly
                forecast_value = prev_forecast * (1 - depreciation_rate)
            
            forecast_values.append(forecast_value)
            actual_values.append(historical_point["value"])
        
        # Calculate metrics
        errors = [abs(f - a) for f, a in zip(forecast_values, actual_values)]
        mae = np.mean(errors)
        mape = np.mean([abs((f - a) / a) * 100 for f, a in zip(forecast_values, actual_values) if a > 0])
        rmse = np.sqrt(np.mean([(f - a) ** 2 for f, a in zip(forecast_values, actual_values)]))
        
        return {
            "mae": round(mae, 2),
            "mape": round(mape, 2),
            "rmse": round(rmse, 2),
            "forecast_values": forecast_values,
            "actual_values": actual_values,
            "data_points": len(historical_after_forecast)
        }
    
    def run_cohort_backtest(
        self,
        model: str,
        trim: str,
        purchase_price: float,
        years: int = 5
    ) -> Dict:
        """Run a complete backtest on a vehicle cohort"""
        # Generate synthetic data
        cohort_data = self.generate_synthetic_cohort_data(model, trim, purchase_price, years)
        
        # Use midpoint as forecast start
        forecast_start_date = datetime.fromisoformat(cohort_data["historical_values"][len(cohort_data["historical_values"]) // 2]["date"])
        
        # Run backtest
        backtest_results = self.backtest_forecast(None, cohort_data, forecast_start_date)
        
        return {
            "cohort": cohort_data,
            "backtest_results": backtest_results,
            "model_performance": {
                "mae": backtest_results.get("mae", 0),
                "mape": backtest_results.get("mape", 0),
                "rmse": backtest_results.get("rmse", 0)
            }
        }
    
    def batch_backtest(
        self,
        models: List[str],
        base_price: float = 30000
    ) -> Dict:
        """Run backtests on multiple vehicle models"""
        results = {}
        
        for model in models:
            result = self.run_cohort_backtest(model, "LE", base_price)
            results[model] = result
        
        # Calculate aggregate metrics
        all_mae = [r["backtest_results"].get("mae", 0) for r in results.values()]
        all_mape = [r["backtest_results"].get("mape", 0) for r in results.values()]
        
        return {
            "individual_results": results,
            "aggregate_metrics": {
                "mean_mae": round(np.mean(all_mae), 2),
                "mean_mape": round(np.mean(all_mape), 2),
                "std_mae": round(np.std(all_mae), 2),
                "std_mape": round(np.std(all_mape), 2)
            }
        }

