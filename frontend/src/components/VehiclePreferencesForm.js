import React, { useState, useEffect } from 'react';
import '../App.css';

function VehiclePreferencesForm({ onSubmit, initialValues }) {
  const [formData, setFormData] = useState({
    make: initialValues?.make || 'Toyota',
    model: initialValues?.model || '',
    trim: initialValues?.trim || '',
    max_price: initialValues?.max_price || '',
    preferred_fuel_type: initialValues?.preferred_fuel_type || ''
  });

  const [models, setModels] = useState([]);
  const [trims, setTrims] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/toyota-models')
      .then(res => res.json())
      .then(data => setModels(data.models))
      .catch(err => console.error('Error fetching models:', err));
  }, []);

  useEffect(() => {
    if (formData.model) {
      const selectedModel = models.find(m => m.name === formData.model);
      if (selectedModel) {
        setTrims(selectedModel.trims);
      }
    }
  }, [formData.model, models]);

  useEffect(() => {
    if (initialValues) {
      setFormData(initialValues);
    }
  }, [initialValues]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    let newData = {
      ...formData,
      [name]: value
    };
    
    if (name === 'model') {
      newData.trim = '';
    }
    
    setFormData(newData);
    
    // Auto-submit when form is complete enough
    if (newData.model) {
      const submitData = {
        ...newData,
        max_price: newData.max_price ? parseFloat(newData.max_price) : null
      };
      onSubmit(submitData);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const submitData = {
      ...formData,
      max_price: formData.max_price ? parseFloat(formData.max_price) : null
    };
    onSubmit(submitData);
  };

  return (
    <div className="card">
      <h3>Vehicle Preferences</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Make</label>
          <input
            type="text"
            name="make"
            value={formData.make}
            disabled
          />
        </div>
        <div className="form-group">
          <label>Model</label>
          <select
            name="model"
            value={formData.model}
            onChange={handleChange}
          >
            <option value="">Select a model</option>
            {models.map(model => (
              <option key={model.name} value={model.name}>
                {model.name}
              </option>
            ))}
          </select>
        </div>
        {formData.model && (
          <div className="form-group">
            <label>Trim</label>
            <select
              name="trim"
              value={formData.trim}
              onChange={handleChange}
            >
              <option value="">Select a trim</option>
              {trims.map(trim => (
                <option key={trim} value={trim}>
                  {trim}
                </option>
              ))}
            </select>
          </div>
        )}
        <div className="form-group">
          <label>Max Price ($) - Optional</label>
          <input
            type="number"
            name="max_price"
            value={formData.max_price}
            onChange={handleChange}
            min="0"
            step="1000"
          />
        </div>
        <div className="form-group">
          <label>Preferred Fuel Type</label>
          <select
            name="preferred_fuel_type"
            value={formData.preferred_fuel_type}
            onChange={handleChange}
          >
            <option value="">No preference</option>
            <option value="gasoline">Gasoline</option>
            <option value="hybrid">Hybrid</option>
            <option value="electric">Electric</option>
          </select>
        </div>
        <button type="submit" style={{ display: 'none' }}>Submit</button>
      </form>
    </div>
  );
}

export default VehiclePreferencesForm;

