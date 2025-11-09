import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import '../App.css';

function ValueForecastChart({ forecast, scenario, onChange }) {
  const [selectedFactors, setSelectedFactors] = useState({
    interest_rate: true,
    fuel_price: true,
    annual_miles: true,
    depreciation: true
  });

  if (!forecast) return null;

  const handleFactorToggle = (factor) => {
    setSelectedFactors(prev => ({
      ...prev,
      [factor]: !prev[factor]
    }));
  };

  // Prepare data for chart
  const chartData = forecast.forecast_curve.map((point, index) => ({
    year: point.year,
    base: point.adjusted_value,
    optimistic: forecast.scenarios.optimistic[index],
    pessimistic: forecast.scenarios.pessimistic[index],
    depreciation: point.depreciation
  }));

  return (
    <div className="card">
      <h3>Value Forecast & Depreciation/Appreciation</h3>
      
      <div style={{ marginBottom: '1rem' }}>
        <h4 style={{ marginBottom: '0.5rem', color: '#666' }}>Adjust Factors:</h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
          {Object.entries(selectedFactors).map(([factor, checked]) => (
            <label key={factor} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={checked}
                onChange={() => handleFactorToggle(factor)}
                style={{ marginRight: '0.5rem' }}
              />
              <span style={{ textTransform: 'capitalize' }}>
                {factor.replace(/_/g, ' ')}
              </span>
            </label>
          ))}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="year" 
            label={{ value: 'Years', position: 'insideBottom', offset: -5 }}
          />
          <YAxis 
            label={{ value: 'Value ($)', angle: -90, position: 'insideLeft' }}
            formatter={(value) => `$${(value / 1000).toFixed(0)}k`}
          />
          <Tooltip 
            formatter={(value) => `$${value.toLocaleString()}`}
            labelFormatter={(label) => `Year ${label}`}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="base" 
            stroke="#667eea" 
            strokeWidth={2}
            name="Base Forecast"
            dot={{ r: 4 }}
          />
          {selectedFactors.interest_rate && (
            <Line 
              type="monotone" 
              dataKey="optimistic" 
              stroke="#4caf50" 
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Optimistic (68% CI)"
              dot={{ r: 3 }}
            />
          )}
          {selectedFactors.fuel_price && (
            <Line 
              type="monotone" 
              dataKey="pessimistic" 
              stroke="#f44336" 
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Pessimistic (68% CI)"
              dot={{ r: 3 }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>

      <div style={{ marginTop: '1.5rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <div style={{ color: '#666', marginBottom: '0.5rem' }}>Initial Value</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
            ${forecast.initial_value.toLocaleString()}
          </div>
        </div>
        <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <div style={{ color: '#666', marginBottom: '0.5rem' }}>Projected Value (5 years)</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#f44336' }}>
            ${forecast.final_value.toLocaleString()}
          </div>
        </div>
        <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <div style={{ color: '#666', marginBottom: '0.5rem' }}>Total Depreciation</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#f44336' }}>
            ${forecast.total_depreciation.toLocaleString()} ({forecast.total_depreciation_percentage.toFixed(1)}%)
          </div>
        </div>
        <div style={{ padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
          <div style={{ color: '#666', marginBottom: '0.5rem' }}>Confidence Score</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#667eea' }}>
            {forecast.confidence_score.toFixed(1)}%
          </div>
        </div>
      </div>

      <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#fff3cd', borderRadius: '8px', fontSize: '0.9rem' }}>
        <strong>Assumptions:</strong> Model: {forecast.factors.model}, 
        Trim: {forecast.factors.trim || 'N/A'}, 
        Annual Miles: {forecast.factors.annual_miles.toLocaleString()}, 
        Interest Rate: {(forecast.factors.interest_rate * 100).toFixed(1)}%, 
        Fuel Price: ${forecast.factors.fuel_price.toFixed(2)}/gal
      </div>
    </div>
  );
}

export default ValueForecastChart;

