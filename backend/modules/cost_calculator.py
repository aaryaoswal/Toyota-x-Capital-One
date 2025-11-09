"""
Monthly Car Cost Cap Calculator
Calculates total monthly cost including payment, insurance, fuel, maintenance, taxes, and fees
"""
from typing import Dict, Optional
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


class CostCalculator:
    """Calculates comprehensive monthly car costs"""
    
    # Average insurance rates by credit score tier
    INSURANCE_MULTIPLIERS = {
        "excellent": 0.8,  # 750+
        "good": 1.0,       # 700-749
        "fair": 1.2,       # 650-699
        "poor": 1.5        # <650
    }
    
    # Base insurance cost (varies by vehicle)
    BASE_INSURANCE_MONTHLY = 120
    
    # Maintenance costs (percentage of vehicle value annually)
    MAINTENANCE_RATE = 0.05  # 5% of vehicle value per year
    
    # Registration and fees (annual)
    REGISTRATION_FEE = 150
    INSPECTION_FEE = 50
    
    # Fuel efficiency by vehicle type (MPG estimates)
    FUEL_EFFICIENCY = {
        "Camry": 32,
        "Corolla": 33,
        "RAV4": 28,
        "Highlander": 24,
        "Prius": 52,
        "4Runner": 17
    }
    
    def __init__(self):
        pass
    
    def get_credit_tier(self, credit_score: int) -> str:
        """Determine credit tier from score"""
        if credit_score >= 750:
            return "excellent"
        elif credit_score >= 700:
            return "good"
        elif credit_score >= 650:
            return "fair"
        else:
            return "poor"
    
    def calculate_apr(self, credit_score: int, base_rate: float = 0.05) -> float:
        """Calculate APR based on credit score"""
        tier = self.get_credit_tier(credit_score)
        adjustments = {
            "excellent": -0.02,  # -2%
            "good": 0.0,
            "fair": 0.02,        # +2%
            "poor": 0.05         # +5%
        }
        return base_rate + adjustments.get(tier, 0.0)
    
    def calculate_monthly_payment(
        self,
        vehicle_price: float,
        down_payment: float,
        apr: float,
        term_months: int
    ) -> float:
        """Calculate monthly loan payment"""
        principal = vehicle_price - down_payment
        if principal <= 0:
            return 0.0
        
        monthly_rate = apr / 12
        if monthly_rate == 0:
            return principal / term_months
        
        payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / \
                  ((1 + monthly_rate) ** term_months - 1)
        return payment
    
    def calculate_lease_payment(
        self,
        vehicle_price: float,
        residual_value: float,
        money_factor: float,
        term_months: int
    ) -> float:
        """Calculate monthly lease payment"""
        depreciation = (vehicle_price - residual_value) / term_months
        finance_charge = (vehicle_price + residual_value) * money_factor
        return depreciation + finance_charge
    
    def calculate_insurance_cost(
        self,
        credit_score: int,
        vehicle_price: float,
        model: Optional[str] = None
    ) -> float:
        """Calculate monthly insurance cost"""
        tier = self.get_credit_tier(credit_score)
        multiplier = self.INSURANCE_MULTIPLIERS.get(tier, 1.0)
        
        # Adjust for vehicle value (higher value = higher insurance)
        price_multiplier = 1 + (vehicle_price / 50000 - 1) * 0.3
        
        base_cost = self.BASE_INSURANCE_MONTHLY * multiplier * price_multiplier
        
        # Model-specific adjustments
        if model == "4Runner" or model == "Highlander":
            base_cost *= 1.1  # SUVs typically cost more to insure
        
        return base_cost
    
    def calculate_fuel_cost(
        self,
        annual_miles: int,
        fuel_price: float,
        model: Optional[str] = None
    ) -> float:
        """Calculate monthly fuel cost"""
        if not model or model not in self.FUEL_EFFICIENCY:
            mpg = 28  # Average
        else:
            mpg = self.FUEL_EFFICIENCY[model]
        
        gallons_per_month = (annual_miles / 12) / mpg
        monthly_fuel_cost = gallons_per_month * fuel_price
        return monthly_fuel_cost
    
    def calculate_maintenance_cost(self, vehicle_price: float) -> float:
        """Calculate monthly maintenance cost"""
        annual_maintenance = vehicle_price * self.MAINTENANCE_RATE
        return annual_maintenance / 12
    
    def calculate_taxes_and_fees(self, vehicle_price: float) -> float:
        """Calculate monthly taxes and fees"""
        # Sales tax (varies by state, using average 7%)
        sales_tax = vehicle_price * 0.07
        
        # Registration and inspection (annual)
        annual_fees = self.REGISTRATION_FEE + self.INSPECTION_FEE
        
        # Amortize over 12 months
        monthly_taxes_fees = (sales_tax + annual_fees) / 12
        return monthly_taxes_fees
    
    def calculate_total_cost(
        self,
        profile: FinancialProfile,
        preferences: VehiclePreferences,
        scenario: ScenarioAdjustments
    ) -> Dict:
        """
        Calculate total monthly car cost cap
        
        Args:
            profile: User's financial profile
            preferences: Vehicle preferences
            scenario: Scenario adjustments
        
        Returns:
            Dictionary with detailed cost breakdown
        """
        # Estimate vehicle price (if not provided, use average)
        if preferences.max_price:
            vehicle_price = preferences.max_price
        else:
            # Default prices by model
            default_prices = {
                "Camry": 28000,
                "Corolla": 22000,
                "RAV4": 32000,
                "Highlander": 38000,
                "Prius": 28000,
                "4Runner": 40000
            }
            vehicle_price = default_prices.get(preferences.model or "Camry", 30000)
        
        # Calculate APR
        base_rate = scenario.interest_rate if scenario.interest_rate else 0.05
        apr = self.calculate_apr(profile.credit_score, base_rate)
        
        # Calculate monthly payment (assuming 10% down payment)
        down_payment = vehicle_price * 0.10
        monthly_payment = self.calculate_monthly_payment(
            vehicle_price, down_payment, apr, profile.lease_term_months
        )
        
        # Calculate insurance
        monthly_insurance = self.calculate_insurance_cost(
            profile.credit_score, vehicle_price, preferences.model
        )
        
        # Calculate fuel cost
        monthly_fuel = self.calculate_fuel_cost(
            scenario.annual_miles, scenario.fuel_price_per_gallon, preferences.model
        )
        
        # Calculate maintenance
        monthly_maintenance = self.calculate_maintenance_cost(vehicle_price)
        
        # Calculate taxes and fees
        monthly_taxes_fees = self.calculate_taxes_and_fees(vehicle_price)
        
        # Total monthly cost
        total_monthly_cost = (
            monthly_payment +
            monthly_insurance +
            monthly_fuel +
            monthly_maintenance +
            monthly_taxes_fees
        )
        
        # Affordability check
        monthly_net_income = (profile.salary + profile.employment_subsidies) / 12
        affordability_ratio = total_monthly_cost / monthly_net_income if monthly_net_income > 0 else 0
        
        return {
            "vehicle_price": round(vehicle_price, 2),
            "down_payment": round(down_payment, 2),
            "apr": round(apr * 100, 2),
            "term_months": profile.lease_term_months,
            "cost_breakdown": {
                "monthly_payment": round(monthly_payment, 2),
                "insurance": round(monthly_insurance, 2),
                "fuel": round(monthly_fuel, 2),
                "maintenance": round(monthly_maintenance, 2),
                "taxes_and_fees": round(monthly_taxes_fees, 2),
                "total": round(total_monthly_cost, 2)
            },
            "affordability": {
                "monthly_net_income": round(monthly_net_income, 2),
                "total_monthly_cost": round(total_monthly_cost, 2),
                "affordability_ratio": round(affordability_ratio * 100, 2),
                "within_budget": total_monthly_cost <= profile.monthly_budget,
                "recommended_max": round(monthly_net_income * 0.20, 2)  # 20% rule
            },
            "assumptions": {
                "down_payment_percentage": 10,
                "maintenance_rate": self.MAINTENANCE_RATE,
                "annual_miles": scenario.annual_miles,
                "fuel_price": scenario.fuel_price_per_gallon
            }
        }

