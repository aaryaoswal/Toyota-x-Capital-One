import React, { useState, useEffect } from 'react';
import '../App.css';

function FinancialProfileForm({ onSubmit, initialValues }) {
  const [formData, setFormData] = useState({
    credit_score: initialValues?.credit_score || 700,
    annual_income: initialValues?.annual_income || 60000,
    monthly_budget: initialValues?.monthly_budget || 500,
    lease_term_months: initialValues?.lease_term_months || 36,
    salary: initialValues?.salary || 60000,
    employment_subsidies: initialValues?.employment_subsidies || 0,
    transportation_subsidy: initialValues?.transportation_subsidy || 0
  });

  useEffect(() => {
    if (initialValues) {
      setFormData(initialValues);
    }
  }, [initialValues]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newData = {
      ...formData,
      [name]: parseFloat(value) || 0
    };
    setFormData(newData);
    onSubmit(newData);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="card">
      <h3>Financial Profile</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Credit Score</label>
          <input
            type="number"
            name="credit_score"
            value={formData.credit_score}
            onChange={handleChange}
            min="300"
            max="850"
            required
          />
        </div>
        <div className="form-group">
          <label>Annual Income ($)</label>
          <input
            type="number"
            name="annual_income"
            value={formData.annual_income}
            onChange={handleChange}
            min="0"
            step="1000"
            required
          />
        </div>
        <div className="form-group">
          <label>Monthly Budget ($)</label>
          <input
            type="number"
            name="monthly_budget"
            value={formData.monthly_budget}
            onChange={handleChange}
            min="0"
            step="50"
            required
          />
        </div>
        <div className="form-group">
          <label>Salary ($)</label>
          <input
            type="number"
            name="salary"
            value={formData.salary}
            onChange={handleChange}
            min="0"
            step="1000"
            required
          />
        </div>
        <div className="form-group">
          <label>Lease Term (months)</label>
          <input
            type="number"
            name="lease_term_months"
            value={formData.lease_term_months}
            onChange={handleChange}
            min="12"
            max="72"
            step="6"
            required
          />
        </div>
        <div className="form-group">
          <label>Employment Subsidies ($)</label>
          <input
            type="number"
            name="employment_subsidies"
            value={formData.employment_subsidies}
            onChange={handleChange}
            min="0"
            step="1000"
          />
        </div>
        <div className="form-group">
          <label>Transportation Subsidy ($)</label>
          <input
            type="number"
            name="transportation_subsidy"
            value={formData.transportation_subsidy}
            onChange={handleChange}
            min="0"
            step="100"
          />
        </div>
        <button type="submit" style={{ display: 'none' }}>Submit</button>
      </form>
    </div>
  );
}

export default FinancialProfileForm;

