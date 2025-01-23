import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    bedrooms: '',
    bathrooms: '',
    sqft: '',
    location: ''
  });

  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (e.target.type === 'number' && value < 0) {
      return; // Prevent negative values
    }
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Ensure no negative values before submitting
    if (formData.bedrooms < 0 || formData.bathrooms < 0 || formData.sqft < 0) {
      alert('Please enter positive values only.');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setPrediction(data.predicted_price);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div className="app-container">
      <h1>House Price Predictor</h1>
      <form className="form-container" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="bedrooms">Bedrooms:</label>
          <input
            type="number"
            id="bedrooms"
            name="bedrooms"
            value={formData.bedrooms}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="bathrooms">Bathrooms:</label>
          <input
            type="number"
            id="bathrooms"
            name="bathrooms"
            value={formData.bathrooms}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="sqft">Square Footage:</label>
          <input
            type="number"
            id="sqft"
            name="sqft"
            value={formData.sqft}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="location">Location:</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="submit-button">Predict Price</button>
      </form>
      {prediction && (
        <div className="prediction-result">
          <h2>Predicted Price:</h2>
          <p>${prediction}</p>
        </div>
      )}
    </div>
  );
}

export default App;
