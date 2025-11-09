import React, { useState } from 'react';
import './App.css';
import FinancialProfileForm from './components/FinancialProfileForm';
import VehiclePreferencesForm from './components/VehiclePreferencesForm';
import ScenarioAdjustments from './components/ScenarioAdjustments';
import ResultsDashboard from './components/ResultsDashboard';
import AffordabilityIndex from './components/AffordabilityIndex';
import ValueForecastChart from './components/ValueForecastChart';
import Recommendations from './components/Recommendations';
import DataSourceInfo from './components/DataSourceInfo';

function App() {
  const [financialProfile, setFinancialProfile] = useState(null);
  const [vehiclePreferences, setVehiclePreferences] = useState(null);
  const [scenario, setScenario] = useState({
    annual_miles: 12000,
    fuel_price_per_gallon: 3.50,
    internship_length_months: null,
    interest_rate: null
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCalculate = async () => {
    if (!financialProfile || !vehiclePreferences) {
      alert('Please fill in all required fields');
      return;
    }

    setLoading(true);
    try {
      // Calculate all metrics
      const [salaryEstimate, monthlyCost, valueForecast, affordability, recommendations] = await Promise.all([
        fetch('http://localhost:8000/api/estimate-salary', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(financialProfile)
        }).then(r => r.json()),
        fetch('http://localhost:8000/api/calculate-monthly-cost', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            profile: financialProfile,
            preferences: vehiclePreferences,
            scenario: scenario
          })
        }).then(r => r.json()),
        fetch('http://localhost:8000/api/forecast-value', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            preferences: vehiclePreferences,
            scenario: scenario,
            years_ahead: 5
          })
        }).then(r => r.json()),
        fetch('http://localhost:8000/api/affordability-index', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            profile: financialProfile,
            preferences: vehiclePreferences,
            scenario: scenario
          })
        }).then(r => r.json()),
        fetch('http://localhost:8000/api/recommendations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            profile: financialProfile,
            preferences: vehiclePreferences,
            scenario: scenario
          })
        }).then(r => r.json())
      ]);

      setResults({
        salaryEstimate,
        monthlyCost,
        valueForecast,
        affordability,
        recommendations
      });
    } catch (error) {
      console.error('Error calculating:', error);
      alert('Error calculating results. Please check that the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Toyota x Capital One</h1>
        <h2>Vehicle Affordability & Value Forecasting Platform</h2>
      </header>

      <div className="container">
        <div className="forms-section">
          <FinancialProfileForm
            onSubmit={setFinancialProfile}
            initialValues={financialProfile}
          />
          <VehiclePreferencesForm
            onSubmit={setVehiclePreferences}
            initialValues={vehiclePreferences}
          />
          <ScenarioAdjustments
            scenario={scenario}
            onChange={setScenario}
          />
          <button
            className="calculate-button"
            onClick={handleCalculate}
            disabled={loading || !financialProfile || !vehiclePreferences}
          >
            {loading ? 'Calculating...' : 'Calculate Affordability & Forecast'}
          </button>
        </div>

        {results && (
          <div className="results-section">
            <AffordabilityIndex affordability={results.affordability} />
            <ResultsDashboard
              salaryEstimate={results.salaryEstimate}
              monthlyCost={results.monthlyCost}
            />
            <ValueForecastChart
              forecast={results.valueForecast}
              scenario={scenario}
              onChange={setScenario}
            />
            <Recommendations recommendations={results.recommendations} />
          </div>
        )}

        <DataSourceInfo />
      </div>
    </div>
  );
}

export default App;

