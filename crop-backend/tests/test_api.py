import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.api.main import app

client = TestClient(app)

class TestAPI:
    """Test cases for the Crop Recommendation API"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert "version" in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_api_health_check(self):
        """Test API health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_predict_crop_valid_input(self):
        """Test crop prediction with valid input"""
        test_input = {
            "N": 90,
            "P": 42,
            "K": 43,
            "temperature": 20.87,
            "humidity": 82.00,
            "ph": 6.50,
            "rainfall": 202.93,
            "ndvi": 0.65
        }
        
        response = client.post("/api/v1/predict", json=test_input)
        
        # Model might not be trained, so we accept both success and model not available
        if response.status_code == 200:
            data = response.json()
            assert "crop" in data
            assert "confidence" in data
            assert "all_probabilities" in data
            assert isinstance(data["confidence"], float)
            assert 0 <= data["confidence"] <= 1
        elif response.status_code == 503:
            # Model not available is acceptable for this test
            assert "Model not available" in response.json()["detail"]
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")
    
    def test_predict_crop_invalid_input(self):
        """Test crop prediction with invalid input"""
        test_input = {
            "N": -10,  # Invalid negative value
            "P": 42,
            "K": 43,
            "temperature": 20.87,
            "humidity": 150,  # Invalid humidity > 100
            "ph": 6.50,
            "rainfall": 202.93
        }
        
        response = client.post("/api/v1/predict", json=test_input)
        assert response.status_code == 422  # Validation error
    
    def test_predict_crop_missing_fields(self):
        """Test crop prediction with missing required fields"""
        test_input = {
            "N": 90,
            "P": 42,
            # Missing required fields
        }
        
        response = client.post("/api/v1/predict", json=test_input)
        assert response.status_code == 422  # Validation error
    
    def test_get_supported_crops(self):
        """Test getting supported crops"""
        response = client.get("/api/v1/crops")
        assert response.status_code == 200
        data = response.json()
        assert "crops" in data
        assert "total" in data
        assert isinstance(data["crops"], list)
    
    def test_get_model_info(self):
        """Test getting model information"""
        response = client.get("/api/v1/model/info")
        
        # Model might not be available
        if response.status_code == 200:
            data = response.json()
            assert "model_type" in data
            assert "n_features" in data
            assert "feature_columns" in data
            assert "n_classes" in data
            assert "classes" in data
        elif response.status_code == 404:
            # Model not found is acceptable
            assert "Model not found" in response.json()["detail"]
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")
    
    def test_sample_prediction(self):
        """Test sample prediction endpoint"""
        response = client.get("/api/v1/predict/sample")
        
        # Model might not be available
        if response.status_code == 200:
            data = response.json()
            assert "input" in data
            assert "prediction" in data
            assert "message" in data
        elif response.status_code == 503:
            # Model not available is acceptable
            assert "Model not available" in response.json()["detail"]
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")

class TestAPIValidation:
    """Test input validation"""
    
    @pytest.mark.parametrize("field,value,should_fail", [
        ("N", -1, True),       # Negative nitrogen
        ("N", 250, True),      # Too high nitrogen
        ("P", -5, True),       # Negative phosphorus
        ("K", 350, True),      # Too high potassium
        ("temperature", -100, True),  # Too low temperature
        ("temperature", 100, True),   # Too high temperature
        ("humidity", -10, True),      # Negative humidity
        ("humidity", 150, True),      # Too high humidity
        ("ph", -1, True),      # Negative pH
        ("ph", 15, True),      # Too high pH
        ("rainfall", -10, True),      # Negative rainfall
        ("ndvi", -2, True),    # Too low NDVI
        ("ndvi", 2, True),     # Too high NDVI
        ("N", 100, False),     # Valid nitrogen
        ("temperature", 25, False),   # Valid temperature
        ("humidity", 75, False),      # Valid humidity
    ])
    def test_field_validation(self, field, value, should_fail):
        """Test individual field validation"""
        base_input = {
            "N": 90,
            "P": 42,
            "K": 43,
            "temperature": 20.87,
            "humidity": 82.00,
            "ph": 6.50,
            "rainfall": 202.93,
            "ndvi": 0.65
        }
        
        # Modify the specific field
        test_input = base_input.copy()
        test_input[field] = value
        
        response = client.post("/api/v1/predict", json=test_input)
        
        if should_fail:
            assert response.status_code == 422, f"Expected validation error for {field}={value}"
        else:
            assert response.status_code in [200, 503], f"Valid input {field}={value} should not fail validation"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])