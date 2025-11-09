import React from 'react';
import '../App.css';

function AffordabilityIndex({ affordability }) {
  if (!affordability) return null;

  const getScoreColor = (score) => {
    if (score >= 90) return '#4caf50';
    if (score >= 75) return '#8bc34a';
    if (score >= 60) return '#ffc107';
    if (score >= 40) return '#ff9800';
    return '#f44336';
  };

  const scoreColor = getScoreColor(affordability.overall_score);

  return (
    <div className="card">
      <h3>Affordability Index</h3>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <div
          style={{
            fontSize: '4rem',
            fontWeight: 'bold',
            color: scoreColor,
            marginBottom: '0.5rem'
          }}
        >
          {affordability.overall_score.toFixed(1)}
        </div>
        <div style={{ fontSize: '1.5rem', color: '#666', marginBottom: '0.5rem' }}>
          {affordability.rating}
        </div>
        <div style={{ color: '#888', fontStyle: 'italic' }}>
          {affordability.recommendation}
        </div>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <h4 style={{ marginBottom: '1rem' }}>Component Scores</h4>
        {Object.entries(affordability.component_scores).map(([key, value]) => (
          <div key={key} style={{ marginBottom: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span style={{ textTransform: 'capitalize', color: '#666' }}>
                {key.replace(/_/g, ' ')}
              </span>
              <span style={{ fontWeight: 'bold', color: getScoreColor(value) }}>
                {value.toFixed(1)}
              </span>
            </div>
            <div
              style={{
                height: '8px',
                backgroundColor: '#e0e0e0',
                borderRadius: '4px',
                overflow: 'hidden'
              }}
            >
              <div
                style={{
                  width: `${value}%`,
                  height: '100%',
                  backgroundColor: getScoreColor(value),
                  transition: 'width 0.3s'
                }}
              />
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <span style={{ color: '#666' }}>Monthly Cost:</span>
          <span style={{ fontWeight: 'bold' }}>${affordability.monthly_cost.toFixed(2)}</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <span style={{ color: '#666' }}>Monthly Income:</span>
          <span style={{ fontWeight: 'bold' }}>${affordability.monthly_income.toFixed(2)}</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span style={{ color: '#666' }}>Debt-to-Income Ratio:</span>
          <span style={{ fontWeight: 'bold' }}>{affordability.debt_to_income_ratio.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
}

export default AffordabilityIndex;

