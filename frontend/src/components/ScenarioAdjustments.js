import React from 'react';
import '../App.css';

function ScenarioAdjustments({ scenario, onChange }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    onChange({
      ...scenario,
      [name]: value ? parseFloat(value) : null
    });
  };

  return (
    <div className="card">
      <h3>Scenario Adjustments</h3>
      <div className="form-group">
        <label>Annual Miles</label>
        <input
          type="number"
          name="annual_miles"
          value={scenario.annual_miles}
          onChange={handleChange}
          min="0"
          step="1000"
        />
      </div>
      <div className="form-group">
        <label>Fuel Price per Gallon ($)</label>
        <input
          type="number"
          name="fuel_price_per_gallon"
          value={scenario.fuel_price_per_gallon}
          onChange={handleChange}
          min="0"
          step="0.10"
        />
      </div>
      <div className="form-group">
        <label>Interest Rate (%) - Optional</label>
        <input
          type="number"
          name="interest_rate"
          value={scenario.interest_rate || ''}
          onChange={handleChange}
          min="0"
          max="20"
          step="0.1"
        />
      </div>
      <div className="form-group">
        <label>Internship Length (months) - Optional</label>
        <input
          type="number"
          name="internship_length_months"
          value={scenario.internship_length_months || ''}
          onChange={handleChange}
          min="0"
          step="1"
        />
      </div>
    </div>
  );
}

export default ScenarioAdjustments;

