"""
Affordability Index Module
Calculates personalized affordability score based on financial profile
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


class AffordabilityIndex:
    """Calculates affordability index score"""
    
    def __init__(self):
        # Weight factors for different components
        self.weights = {
            "debt_to_income": 0.30,
            "credit_score": 0.25,
            "budget_alignment": 0.20,
            "income_stability": 0.15,
            "term_appropriateness": 0.10
        }
    
    def calculate_debt_to_income_score(
        self,
        monthly_cost: float,
        monthly_income: float
    ) -> float:
        """Calculate score based on debt-to-income ratio"""
        if monthly_income <= 0:
            return 0.0
        
        dti_ratio = monthly_cost / monthly_income
        
        # Ideal DTI is 15-20% for car payments
        if dti_ratio <= 0.15:
            return 100.0
        elif dti_ratio <= 0.20:
            return 90.0
        elif dti_ratio <= 0.25:
            return 75.0
        elif dti_ratio <= 0.30:
            return 60.0
        elif dti_ratio <= 0.35:
            return 40.0
        else:
            # Penalize heavily for DTI > 35%
            return max(0, 40.0 - (dti_ratio - 0.35) * 200)
    
    def calculate_credit_score_rating(self, credit_score: int) -> float:
        """Calculate score based on credit score"""
        if credit_score >= 750:
            return 100.0
        elif credit_score >= 700:
            return 85.0
        elif credit_score >= 650:
            return 70.0
        elif credit_score >= 600:
            return 50.0
        else:
            return max(0, 30.0 + (credit_score - 500) * 0.4)
    
    def calculate_budget_alignment_score(
        self,
        monthly_cost: float,
        monthly_budget: float
    ) -> float:
        """Calculate score based on budget alignment"""
        if monthly_budget <= 0:
            return 0.0
        
        if monthly_cost <= monthly_budget:
            # Bonus for being under budget
            if monthly_cost <= monthly_budget * 0.8:
                return 100.0
            else:
                # Linear scale from 80% to 100% of budget
                ratio = (monthly_budget - monthly_cost) / (monthly_budget * 0.2)
                return 80.0 + (ratio * 20.0)
        else:
            # Penalty for exceeding budget
            excess_ratio = (monthly_cost - monthly_budget) / monthly_budget
            return max(0, 80.0 - (excess_ratio * 100))
    
    def calculate_income_stability_score(
        self,
        salary: float,
        employment_subsidies: float
    ) -> float:
        """Calculate score based on income stability"""
        # Higher base salary = more stable
        if salary >= 100000:
            base_score = 100.0
        elif salary >= 75000:
            base_score = 90.0
        elif salary >= 50000:
            base_score = 80.0
        elif salary >= 35000:
            base_score = 70.0
        else:
            base_score = 60.0
        
        # Subsidies add some uncertainty (but still positive)
        if employment_subsidies > 0:
            subsidy_ratio = employment_subsidies / (salary + employment_subsidies)
            # Small penalty for high reliance on subsidies
            adjustment = -subsidy_ratio * 10
            base_score += adjustment
        
        return max(0, min(100, base_score))
    
    def calculate_term_appropriateness_score(
        self,
        lease_term_months: int,
        monthly_cost: float,
        monthly_income: float
    ) -> float:
        """Calculate score based on lease term appropriateness"""
        # Longer terms = lower monthly payment but more interest
        # Ideal term is 36-48 months for most vehicles
        
        if 36 <= lease_term_months <= 48:
            return 100.0
        elif 24 <= lease_term_months < 36:
            return 90.0
        elif 48 < lease_term_months <= 60:
            return 85.0
        elif lease_term_months > 60:
            # Very long terms are risky
            return max(0, 85.0 - (lease_term_months - 60) * 2)
        else:
            # Very short terms may be too expensive monthly
            return max(0, 70.0 - (36 - lease_term_months) * 3)
    
    def calculate(
        self,
        profile: FinancialProfile,
        preferences: VehiclePreferences,
        scenario: ScenarioAdjustments,
        monthly_cost: float = None
    ) -> Dict:
        """
        Calculate affordability index score
        
        Args:
            profile: User's financial profile
            preferences: Vehicle preferences
            scenario: Scenario adjustments
            monthly_cost: Pre-calculated monthly cost (optional)
        
        Returns:
            Dictionary with affordability index and breakdown
        """
        # Calculate monthly income
        monthly_income = (profile.salary + profile.employment_subsidies) / 12
        
        # If monthly cost not provided, estimate it
        if monthly_cost is None:
            # Simple estimation
            if preferences.max_price:
                vehicle_price = preferences.max_price
            else:
                default_prices = {
                    "Camry": 28000,
                    "Corolla": 22000,
                    "RAV4": 32000,
                    "Highlander": 38000,
                    "Prius": 28000,
                    "4Runner": 40000
                }
                vehicle_price = default_prices.get(preferences.model or "Camry", 30000)
            
            # Rough estimate: 1% of vehicle price per month
            monthly_cost = vehicle_price * 0.01
        
        # Calculate component scores
        dti_score = self.calculate_debt_to_income_score(monthly_cost, monthly_income)
        credit_score = self.calculate_credit_score_rating(profile.credit_score)
        budget_score = self.calculate_budget_alignment_score(monthly_cost, profile.monthly_budget)
        income_stability_score = self.calculate_income_stability_score(
            profile.salary, profile.employment_subsidies
        )
        term_score = self.calculate_term_appropriateness_score(
            profile.lease_term_months, monthly_cost, monthly_income
        )
        
        # Calculate weighted overall score
        overall_score = (
            dti_score * self.weights["debt_to_income"] +
            credit_score * self.weights["credit_score"] +
            budget_score * self.weights["budget_alignment"] +
            income_stability_score * self.weights["income_stability"] +
            term_score * self.weights["term_appropriateness"]
        )
        
        # Determine rating
        if overall_score >= 90:
            rating = "Excellent"
            recommendation = "Highly recommended"
        elif overall_score >= 75:
            rating = "Good"
            recommendation = "Recommended with minor adjustments"
        elif overall_score >= 60:
            rating = "Fair"
            recommendation = "Consider reducing vehicle price or increasing down payment"
        elif overall_score >= 40:
            rating = "Poor"
            recommendation = "Not recommended - consider more affordable options"
        else:
            rating = "Very Poor"
            recommendation = "Strongly not recommended - financial risk too high"
        
        return {
            "overall_score": round(overall_score, 2),
            "rating": rating,
            "recommendation": recommendation,
            "component_scores": {
                "debt_to_income": round(dti_score, 2),
                "credit_score": round(credit_score, 2),
                "budget_alignment": round(budget_score, 2),
                "income_stability": round(income_stability_score, 2),
                "term_appropriateness": round(term_score, 2)
            },
            "weights": self.weights,
            "monthly_cost": round(monthly_cost, 2),
            "monthly_income": round(monthly_income, 2),
            "debt_to_income_ratio": round((monthly_cost / monthly_income) * 100, 2) if monthly_income > 0 else 0
        }

