import pytest
from app import app, preload_model

def test_preload_model():
    """Test that the model is preloaded successfully."""
    try:
        preload_model()
    except Exception as e:
        pytest.fail(f"Model preload failed: {str(e)}")

def test_predict_route():
    """Test the predict route with valid input."""
    client = app.test_client()
    response = client.post('/predict', json={
        "area": 1200, "bedrooms": 2, "bathrooms": 1, "stories": 1,
        "mainroad": "yes", "guestroom": "no", "basement": "no",
        "hotwaterheating": "no", "airconditioning": "no",
        "parking": 1, "prefarea": "no", "furnishingstatus": "semi-furnished"
    })
    assert response.status_code == 200
    assert "predicted_price" in response.get_json()

def test_predict_route_invalid_input():
    """Test the predict route with invalid input."""
    client = app.test_client()
    response = client.post('/predict', json={})
    assert response.status_code == 400
    assert "error" in response.get_json()
