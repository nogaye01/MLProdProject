import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    area: '',
    bedrooms: '',
    bathrooms: '',
    stories: '',
    mainroad: '',
    guestroom: '',
    basement: '',
    hotwaterheating: '',
    airconditioning: '',
    parking: '',
    prefarea: '',
    furnishingstatus: '',
  });

  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (data.error) {
        alert(`Error: ${data.error}`);
      } else {
        setPrediction(data.predicted_price);
      }
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div className="app-container">
      <h1>House Price Predictor</h1>
      <form className="form-container" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="area">Area:</label>
          <input
            type="number"
            id="area"
            name="area"
            value={formData.area}
            onChange={handleChange}
            required
          />
        </div>
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
          <label htmlFor="stories">Stories:</label>
          <input
            type="number"
            id="stories"
            name="stories"
            value={formData.stories}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="mainroad">Main Road:</label>
          <select
            id="mainroad"
            name="mainroad"
            value={formData.mainroad}
            onChange={handleChange}
            required
          >
            <option value="">Select</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="guestroom">Guest Room:</label>
          <select
            id="guestroom"
            name="guestroom"
            value={formData.guestroom}
            onChange={handleChange}
            required
          >
            <option value="">Select</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="basement">Basement:</label>
          <select
            id="basement"
            name="basement"
            value={formData.basement}
            onChange={handleChange}
            required
          >
            <option value="">Select</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="hotwaterheating">Hot Water Heating:</label>
          <select
            id="hotwaterheating"
            name="hotwaterheating"
            value={formData.hotwaterheating}
            onChange={handleChange}
            required
          >
            <option value="">Select</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="airconditioning">Air Conditioning:</label>
          <select
            id="airconditioning"
            name="airconditioning"
            value={formData.airconditioning}
            onChange={handleChange}
            required
          >
            <option value="">Select</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="parking">Parking:</label>
          <input
            type="number"
            id="parking"
            name="parking"
            value={formData.parking}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="prefarea">Preferred Area:</label>
          <select
            id="prefarea"   
            name="prefarea"
            value={formData.prefarea}
            onChange={handleChange}
            required
          >
            <option value="">Select</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="furnishingstatus">Furnishing Status:</label>
          <select
            id="furnishingstatus" 
            name="furnishingstatus"
            value={formData.furnishingstatus}
            onChange={handleChange}
            required
          >
            <option value="">Select</option>
            <option value="furnished">Furnished</option>
            <option value="semi-furnished">Semi-Furnished</option>
            <option value="unfurnished">Unfurnished</option>
          </select>
        </div>
        <button type="submit" className="submit-button">
          Predict Price
        </button>
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