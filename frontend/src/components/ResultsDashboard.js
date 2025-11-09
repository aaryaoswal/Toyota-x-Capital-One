import React from 'react';
import '../App.css';

function ResultsDashboard({ salaryEstimate, monthlyCost }) {
  if (!salaryEstimate || !monthlyCost) return null;

  return (
    <div className="card">
      <h3>Financial Summary</h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
        <div>
          <h4 style={{ marginBottom: '1rem', color: '#666' }}>Net Pay Estimate</h4>
          <div style={{ marginBottom: '0.5rem' }}>
            <span style={{ color: '#666' }}>Monthly Net:</span>
            <span style={{ float: 'right', fontWeight: 'bold' }}>
              ${salaryEstimate.monthly_net.toFixed(2)}
            </span>
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <span style={{ color: '#666' }}>Conservative Monthly:</span>
            <span style={{ float: 'right', fontWeight: 'bold', color: '#ff9800' }}>
              ${salaryEstimate.conservative_monthly_net.toFixed(2)}
            </span>
          </div>
          <div style={{ fontSize: '0.9rem', color: '#888', marginTop: '0.5rem' }}>
            Volatility: {salaryEstimate.volatility_percentage.toFixed(1)}%
          </div>
        </div>

        <div>
          <h4 style={{ marginBottom: '1rem', color: '#666' }}>Monthly Car Costs</h4>
          <div style={{ marginBottom: '0.5rem' }}>
            <span style={{ color: '#666' }}>Payment:</span>
            <span style={{ float: 'right', fontWeight: 'bold' }}>
              ${monthlyCost.cost_breakdown.monthly_payment.toFixed(2)}
            </span>
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <span style={{ color: '#666' }}>Insurance:</span>
            <span style={{ float: 'right' }}>
              ${monthlyCost.cost_breakdown.insurance.toFixed(2)}
            </span>
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <span style={{ color: '#666' }}>Fuel:</span>
            <span style={{ float: 'right' }}>
              ${monthlyCost.cost_breakdown.fuel.toFixed(2)}
            </span>
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <span style={{ color: '#666' }}>Maintenance:</span>
            <span style={{ float: 'right' }}>
              ${monthlyCost.cost_breakdown.maintenance.toFixed(2)}
            </span>
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <span style={{ color: '#666' }}>Taxes & Fees:</span>
            <span style={{ float: 'right' }}>
              ${monthlyCost.cost_breakdown.taxes_and_fees.toFixed(2)}
            </span>
          </div>
          <div style={{ 
            marginTop: '0.5rem', 
            paddingTop: '0.5rem', 
            borderTop: '2px solid #e0e0e0',
            fontWeight: 'bold',
            fontSize: '1.1rem'
          }}>
            <span>Total:</span>
            <span style={{ float: 'right', color: '#667eea' }}>
              ${monthlyCost.cost_breakdown.total.toFixed(2)}
            </span>
          </div>
        </div>
      </div>

      <div style={{ 
        padding: '1rem', 
        backgroundColor: monthlyCost.affordability.within_budget ? '#e8f5e9' : '#ffebee',
        borderRadius: '8px',
        border: `2px solid ${monthlyCost.affordability.within_budget ? '#4caf50' : '#f44336'}`
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <span style={{ fontWeight: 'bold' }}>Within Budget:</span>
          <span style={{ 
            fontWeight: 'bold',
            color: monthlyCost.affordability.within_budget ? '#4caf50' : '#f44336'
          }}>
            {monthlyCost.affordability.within_budget ? 'Yes ✓' : 'No ✗'}
          </span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <span>Affordability Ratio:</span>
          <span style={{ fontWeight: 'bold' }}>
            {monthlyCost.affordability.affordability_ratio.toFixed(1)}%
          </span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>Recommended Max:</span>
          <span style={{ fontWeight: 'bold' }}>
            ${monthlyCost.affordability.recommended_max.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  );
}

export default ResultsDashboard;

