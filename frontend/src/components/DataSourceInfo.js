import React, { useState, useEffect } from 'react';
import '../App.css';

function DataSourceInfo() {
  const [dataSources, setDataSources] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/data-sources')
      .then(res => res.json())
      .then(data => setDataSources(data))
      .catch(err => console.error('Error fetching data sources:', err));
  }, []);

  if (!dataSources) return null;

  return (
    <div className="card" style={{ gridColumn: '1 / -1' }}>
      <h3>Data Sources & Compliance</h3>
      <p style={{ color: '#666', marginBottom: '1rem', fontStyle: 'italic' }}>
        {dataSources.disclaimer}
      </p>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
        {dataSources.sources.map((source, index) => (
          <div
            key={index}
            style={{
              padding: '1rem',
              backgroundColor: '#f5f5f5',
              borderRadius: '8px',
              border: '1px solid #e0e0e0'
            }}
          >
            <div style={{ fontWeight: 'bold', marginBottom: '0.5rem', color: '#667eea' }}>
              {source.name}
            </div>
            <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.25rem' }}>
              Type: <strong>{source.type}</strong>
            </div>
            <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.25rem' }}>
              Refresh: <strong>{source.refresh_cadence}</strong>
            </div>
            <div style={{ fontSize: '0.85rem', color: '#888' }}>
              Last Updated: {source.last_updated ? new Date(source.last_updated).toLocaleDateString() : 'N/A'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DataSourceInfo;

