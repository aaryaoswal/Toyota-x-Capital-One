import React from 'react';
import '../App.css';

function Recommendations({ recommendations }) {
  if (!recommendations || !recommendations.recommendations) return null;

  return (
    <div className="card">
      <h3>Personalized Recommendations</h3>
      <p style={{ color: '#666', marginBottom: '1rem' }}>
        Top {recommendations.recommendations.length} recommendations based on your profile
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {recommendations.recommendations.map((rec, index) => (
          <div
            key={index}
            style={{
              padding: '1.5rem',
              backgroundColor: index === 0 ? '#e3f2fd' : '#f5f5f5',
              borderRadius: '8px',
              border: index === 0 ? '2px solid #667eea' : '1px solid #e0e0e0'
            }}
          >
            {index === 0 && (
              <div style={{ 
                display: 'inline-block',
                padding: '0.25rem 0.75rem',
                backgroundColor: '#667eea',
                color: 'white',
                borderRadius: '4px',
                fontSize: '0.9rem',
                fontWeight: 'bold',
                marginBottom: '0.5rem'
              }}>
                BEST MATCH
              </div>
            )}
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <div>
                <h4 style={{ fontSize: '1.3rem', marginBottom: '0.25rem' }}>
                  {rec.model} {rec.trim}
                </h4>
                <div style={{ color: '#666', fontSize: '0.9rem' }}>
                  Overall Score: <strong style={{ color: '#667eea' }}>{rec.overall_score.toFixed(1)}</strong>
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#667eea' }}>
                  ${rec.price.toLocaleString()}
                </div>
                <div style={{ color: '#666', fontSize: '0.9rem' }}>
                  ${rec.monthly_payment.toFixed(2)}/month
                </div>
              </div>
            </div>

            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(3, 1fr)', 
              gap: '1rem',
              marginBottom: '1rem',
              padding: '1rem',
              backgroundColor: 'white',
              borderRadius: '6px'
            }}>
              <div>
                <div style={{ color: '#666', fontSize: '0.85rem', marginBottom: '0.25rem' }}>Personal Match</div>
                <div style={{ fontWeight: 'bold', color: '#4caf50' }}>
                  {rec.personal_percentage_match.toFixed(1)}%
                </div>
              </div>
              <div>
                <div style={{ color: '#666', fontSize: '0.85rem', marginBottom: '0.25rem' }}>Reliability</div>
                <div style={{ fontWeight: 'bold', color: '#2196f3' }}>
                  {rec.reliability_score.toFixed(0)}/100
                </div>
              </div>
              <div>
                <div style={{ color: '#666', fontSize: '0.85rem', marginBottom: '0.25rem' }}>APR</div>
                <div style={{ fontWeight: 'bold', color: '#ff9800' }}>
                  {rec.apr.toFixed(2)}%
                </div>
              </div>
            </div>

            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(2, 1fr)', 
              gap: '0.5rem',
              fontSize: '0.9rem',
              color: '#666'
            }}>
              <div>Fuel Efficiency: <strong>{rec.fuel_efficiency} MPG</strong></div>
              <div>Residual Value: <strong>${rec.residual_value.toLocaleString()}</strong></div>
              <div>Down Payment: <strong>${rec.down_payment.toLocaleString()}</strong></div>
              <div>Residual %: <strong>{rec.residual_percentage.toFixed(1)}%</strong></div>
            </div>

            <div style={{ 
              marginTop: '1rem', 
              padding: '0.75rem', 
              backgroundColor: '#fff3cd', 
              borderRadius: '6px',
              fontSize: '0.85rem'
            }}>
              <strong>Factors:</strong> Salary Match: {rec.factors.salary_match.toFixed(1)}%, 
              Budget Match: {rec.factors.budget_match.toFixed(1)}%, 
              Credit Score: {rec.factors.credit_score}
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#e8f5e9', borderRadius: '8px' }}>
        <div style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Scoring Weights:</div>
        <div style={{ fontSize: '0.9rem', color: '#666' }}>
          Personal Match: {(recommendations.scoring_weights.personal_match * 100).toFixed(0)}%, 
          Reliability: {(recommendations.scoring_weights.reliability * 100).toFixed(0)}%, 
          Affordability: {(recommendations.scoring_weights.affordability * 100).toFixed(0)}%
        </div>
      </div>
    </div>
  );
}

export default Recommendations;

