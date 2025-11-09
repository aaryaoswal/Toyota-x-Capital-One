"""
Personalized Recommendation Engine
Generates vehicle recommendations based on APR matching, percentage match, and reliability
"""
from typing import Dict, List, Optional
from pydantic import BaseModel
import math


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


class RecommendationEngine:
    """Generates personalized vehicle recommendations"""
    
    # Toyota vehicle database
    TOYOTA_VEHICLES = [
        {
            "model": "Camry",
            "trims": ["LE", "SE", "XLE", "XSE"],
            "base_price": 26500,
            "reliability_score": 95,
            "fuel_efficiency": 32,
            "residual_value_36mo": 0.60,
            "residual_value_48mo": 0.50
        },
        {
            "model": "Corolla",
            "trims": ["L", "LE", "SE", "XLE", "XSE"],
            "base_price": 21500,
            "reliability_score": 98,
            "fuel_efficiency": 33,
            "residual_value_36mo": 0.65,
            "residual_value_48mo": 0.55
        },
        {
            "model": "RAV4",
            "trims": ["LE", "XLE", "XLE Premium", "Limited", "Adventure"],
            "base_price": 31000,
            "reliability_score": 92,
            "fuel_efficiency": 28,
            "residual_value_36mo": 0.58,
            "residual_value_48mo": 0.48
        },
        {
            "model": "Highlander",
            "trims": ["L", "LE", "XLE", "Limited", "Platinum"],
            "base_price": 36500,
            "reliability_score": 90,
            "fuel_efficiency": 24,
            "residual_value_36mo": 0.55,
            "residual_value_48mo": 0.45
        },
        {
            "model": "Prius",
            "trims": ["LE", "XLE", "Limited"],
            "base_price": 27500,
            "reliability_score": 96,
            "fuel_efficiency": 52,
            "residual_value_36mo": 0.62,
            "residual_value_48mo": 0.52
        },
        {
            "model": "4Runner",
            "trims": ["SR5", "TRD Off-Road", "Limited", "TRD Pro"],
            "base_price": 38500,
            "reliability_score": 94,
            "fuel_efficiency": 17,
            "residual_value_36mo": 0.70,
            "residual_value_48mo": 0.60
        }
    ]
    
    # Trim price multipliers
    TRIM_MULTIPLIERS = {
        "L": 1.0,
        "LE": 1.05,
        "SE": 1.10,
        "XLE": 1.15,
        "XSE": 1.12,
        "Limited": 1.20,
        "Platinum": 1.25,
        "Adventure": 1.18,
        "TRD Off-Road": 1.22,
        "TRD Pro": 1.30,
        "XLE Premium": 1.18
    }
    
    def __init__(self):
        pass
    
    def calculate_apr(self, credit_score: int, base_rate: float = 0.05) -> float:
        """Calculate APR based on credit score"""
        if credit_score >= 750:
            return base_rate - 0.02
        elif credit_score >= 700:
            return base_rate
        elif credit_score >= 650:
            return base_rate + 0.02
        else:
            return base_rate + 0.05
    
    def calculate_personal_percentage_match(
        self,
        vehicle_price: float,
        monthly_budget: float,
        monthly_income: float,
        apr: float,
        term_months: int
    ) -> float:
        """Calculate how well the vehicle matches personal financial situation"""
        # Calculate monthly payment
        down_payment = vehicle_price * 0.10
        principal = vehicle_price - down_payment
        monthly_rate = apr / 12
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / \
                         ((1 + monthly_rate) ** term_months - 1)
        
        # Budget match (0-50 points)
        if monthly_payment <= monthly_budget:
            budget_match = 50.0
        else:
            excess = monthly_payment - monthly_budget
            budget_match = max(0, 50.0 - (excess / monthly_budget) * 50)
        
        # Income match (0-30 points) - ideal is 15-20% of income
        payment_ratio = monthly_payment / monthly_income if monthly_income > 0 else 1.0
        if 0.15 <= payment_ratio <= 0.20:
            income_match = 30.0
        elif payment_ratio < 0.15:
            income_match = 30.0 * (payment_ratio / 0.15)
        else:
            income_match = max(0, 30.0 - (payment_ratio - 0.20) * 300)
        
        # APR match (0-20 points) - lower is better
        if apr <= 0.03:
            apr_match = 20.0
        elif apr <= 0.05:
            apr_match = 15.0
        elif apr <= 0.07:
            apr_match = 10.0
        else:
            apr_match = max(0, 10.0 - (apr - 0.07) * 100)
        
        return budget_match + income_match + apr_match
    
    def calculate_reliability_score(
        self,
        base_reliability: int,
        term_months: int
    ) -> float:
        """Calculate reliability score based on lease term"""
        # Longer terms = higher reliability needed
        if term_months <= 36:
            reliability_multiplier = 1.0
        elif term_months <= 48:
            reliability_multiplier = 1.05
        else:
            reliability_multiplier = 1.10
        
        # Base reliability is already high for Toyotas
        adjusted_reliability = base_reliability * reliability_multiplier
        
        # Cap at 100
        return min(100, adjusted_reliability)
    
    def generate_recommendations(
        self,
        profile: FinancialProfile,
        preferences: VehiclePreferences,
        scenario: ScenarioAdjustments
    ) -> Dict:
        """
        Generate personalized vehicle recommendations
        
        Args:
            profile: User's financial profile
            preferences: Vehicle preferences
            scenario: Scenario adjustments
        
        Returns:
            Dictionary with ranked recommendations
        """
        monthly_income = (profile.salary + profile.employment_subsidies) / 12
        apr = self.calculate_apr(profile.credit_score, scenario.interest_rate or 0.05)
        
        recommendations = []
        
        # Filter vehicles based on preferences
        candidate_vehicles = self.TOYOTA_VEHICLES
        if preferences.model:
            candidate_vehicles = [v for v in candidate_vehicles if v["model"] == preferences.model]
        
        # Generate recommendations for each vehicle/trim combination
        for vehicle in candidate_vehicles:
            for trim in vehicle["trims"]:
                # Calculate vehicle price
                trim_multiplier = self.TRIM_MULTIPLIERS.get(trim, 1.0)
                vehicle_price = vehicle["base_price"] * trim_multiplier
                
                # Check if within max price constraint
                if preferences.max_price and vehicle_price > preferences.max_price:
                    continue
                
                # Calculate personal percentage match
                personal_match = self.calculate_personal_percentage_match(
                    vehicle_price,
                    profile.monthly_budget,
                    monthly_income,
                    apr,
                    profile.lease_term_months
                )
                
                # Calculate reliability score
                reliability = self.calculate_reliability_score(
                    vehicle["reliability_score"],
                    profile.lease_term_months
                )
                
                # Calculate monthly payment
                down_payment = vehicle_price * 0.10
                principal = vehicle_price - down_payment
                monthly_rate = apr / 12
                monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** profile.lease_term_months) / \
                                 ((1 + monthly_rate) ** profile.lease_term_months - 1)
                
                # Calculate residual value
                if profile.lease_term_months <= 36:
                    residual_pct = vehicle["residual_value_36mo"]
                else:
                    residual_pct = vehicle["residual_value_48mo"]
                
                residual_value = vehicle_price * residual_pct
                
                # Overall recommendation score
                overall_score = (
                    personal_match * 0.50 +  # 50% weight on personal match
                    reliability * 0.30 +      # 30% weight on reliability
                    (100 - (monthly_payment / monthly_income * 100)) * 0.20 if monthly_income > 0 else 0  # 20% on affordability
                )
                
                recommendations.append({
                    "model": vehicle["model"],
                    "trim": trim,
                    "price": round(vehicle_price, 2),
                    "monthly_payment": round(monthly_payment, 2),
                    "apr": round(apr * 100, 2),
                    "personal_percentage_match": round(personal_match, 2),
                    "reliability_score": round(reliability, 2),
                    "overall_score": round(overall_score, 2),
                    "fuel_efficiency": vehicle["fuel_efficiency"],
                    "residual_value": round(residual_value, 2),
                    "residual_percentage": round(residual_pct * 100, 2),
                    "down_payment": round(down_payment, 2),
                    "factors": {
                        "salary_match": round((monthly_payment / monthly_income) * 100, 2) if monthly_income > 0 else 0,
                        "budget_match": round((monthly_payment / profile.monthly_budget) * 100, 2) if profile.monthly_budget > 0 else 0,
                        "credit_score": profile.credit_score,
                        "lease_term": profile.lease_term_months
                    }
                })
        
        # Sort by overall score
        recommendations.sort(key=lambda x: x["overall_score"], reverse=True)
        
        # Limit to top 10
        top_recommendations = recommendations[:10]
        
        return {
            "recommendations": top_recommendations,
            "total_options": len(recommendations),
            "user_profile": {
                "credit_score": profile.credit_score,
                "monthly_income": round(monthly_income, 2),
                "monthly_budget": profile.monthly_budget,
                "apr": round(apr * 100, 2)
            },
            "scoring_weights": {
                "personal_match": 0.50,
                "reliability": 0.30,
                "affordability": 0.20
            }
        }

