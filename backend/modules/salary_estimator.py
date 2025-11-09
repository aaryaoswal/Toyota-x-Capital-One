"""
Salary and Net Pay Estimation Module
Estimates conservative net pay and volatility from salary data
"""
import numpy as np
from typing import Dict, Optional
from datetime import datetime


class SalaryEstimator:
    """Estimates net pay and volatility from salary and employment data"""
    
    # Tax brackets (simplified - federal only, 2024)
    TAX_BRACKETS = [
        (0, 0.10),
        (11000, 0.12),
        (44725, 0.22),
        (95375, 0.24),
        (201050, 0.32),
        (243725, 0.35),
        (609350, 0.37)
    ]
    
    # Average state tax rate (simplified)
    STATE_TAX_RATE = 0.05
    
    # FICA rates
    SOCIAL_SECURITY_RATE = 0.062
    MEDICARE_RATE = 0.0145
    FICA_CAP = 168600  # 2024 Social Security wage base
    
    def __init__(self):
        self.volatility_factor = 0.15  # 15% volatility assumption
    
    def calculate_federal_tax(self, income: float) -> float:
        """Calculate federal income tax"""
        tax = 0.0
        remaining_income = income
        
        for i in range(len(self.TAX_BRACKETS) - 1, -1, -1):
            bracket_min, rate = self.TAX_BRACKETS[i]
            if remaining_income > bracket_min:
                if i == len(self.TAX_BRACKETS) - 1:
                    # Top bracket
                    tax += (remaining_income - bracket_min) * rate
                else:
                    next_bracket_min, _ = self.TAX_BRACKETS[i + 1]
                    taxable_in_bracket = min(remaining_income, next_bracket_min) - bracket_min
                    tax += taxable_in_bracket * rate
                    remaining_income = bracket_min
        
        return tax
    
    def calculate_fica(self, income: float) -> float:
        """Calculate FICA taxes"""
        social_security = min(income, self.FICA_CAP) * self.SOCIAL_SECURITY_RATE
        medicare = income * self.MEDICARE_RATE
        return social_security + medicare
    
    def estimate(
        self,
        annual_salary: float,
        employment_subsidies: float = 0.0,
        transportation_subsidy: float = 0.0
    ) -> Dict:
        """
        Estimate net pay and volatility
        
        Args:
            annual_salary: Annual gross salary
            employment_subsidies: Additional employment benefits (taxable)
            transportation_subsidy: Transportation subsidy (may be non-taxable)
        
        Returns:
            Dictionary with net pay estimates and volatility metrics
        """
        # Total gross income
        gross_income = annual_salary + employment_subsidies
        
        # Calculate taxes
        federal_tax = self.calculate_federal_tax(gross_income)
        state_tax = gross_income * self.STATE_TAX_RATE
        fica = self.calculate_fica(gross_income)
        
        total_taxes = federal_tax + state_tax + fica
        
        # Net pay (conservative estimate)
        net_pay = gross_income - total_taxes + transportation_subsidy
        
        # Monthly breakdown
        monthly_gross = gross_income / 12
        monthly_net = net_pay / 12
        
        # Volatility calculation (simulate income variability)
        volatility = net_pay * self.volatility_factor
        
        # Conservative estimate (subtract one standard deviation)
        conservative_net_pay = net_pay - volatility
        
        # Confidence intervals
        confidence_95_low = net_pay - (volatility * 1.96)
        confidence_95_high = net_pay + (volatility * 1.96)
        
        return {
            "gross_annual": round(gross_income, 2),
            "net_annual": round(net_pay, 2),
            "conservative_net_annual": round(max(0, conservative_net_pay), 2),
            "monthly_gross": round(monthly_gross, 2),
            "monthly_net": round(monthly_net, 2),
            "conservative_monthly_net": round(max(0, conservative_net_pay / 12), 2),
            "volatility": round(volatility, 2),
            "volatility_percentage": round((volatility / net_pay) * 100, 2) if net_pay > 0 else 0,
            "tax_breakdown": {
                "federal": round(federal_tax, 2),
                "state": round(state_tax, 2),
                "fica": round(fica, 2),
                "total": round(total_taxes, 2)
            },
            "confidence_intervals": {
                "95_low": round(max(0, confidence_95_low), 2),
                "95_high": round(confidence_95_high, 2)
            },
            "last_updated": datetime.now().isoformat()
        }

