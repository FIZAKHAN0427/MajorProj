import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.model import CropModel
from src.preprocessing import create_sample_data, prepare_features_target

class TestCropModel:
    """Test cases for the CropModel class"""
    
    @pytest.fixture
    def model(self):
        """Create a fresh model instance for testing"""
        return CropModel()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        return create_sample_data()
    
    @pytest.fixture
    def temp_model_path(self):
        """Create a temporary path for model storage"""
        temp_dir = tempfile.mkdtemp()
        model_path = Path(temp_dir) / "test_model.pkl"
        yield model_path
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_model_initialization(self, model):
        """Test model initialization"""
        assert model.model is None
        assert model.label_encoder is not None
        assert isinstance(model.feature_columns, list)
        assert len(model.feature_columns) > 0
    
    def test_model_training(self, model, sample_data):
        """Test model training"""
        # Train the model
        results = model.train(test_size=0.3, random_state=42)
        
        # Check that model is trained
        assert model.model is not None
        assert hasattr(model.model, 'predict')
        
        # Check training results
        assert isinstance(results, dict)
        assert 'train_accuracy' in results
        assert 'test_accuracy' in results
        assert 'cv_mean' in results
        assert 'cv_std' in results
        assert 'feature_importance' in results
        
        # Check accuracy values are reasonable
        assert 0 <= results['train_accuracy'] <= 1
        assert 0 <= results['test_accuracy'] <= 1
        assert 0 <= results['cv_mean'] <= 1
    
    def test_model_prediction(self, model, sample_data):
        """Test model prediction"""
        # Train the model first
        model.train(test_size=0.3, random_state=42)
        
        # Test single prediction
        test_input = {
            'N': 90, 'P': 42, 'K': 43,
            'temperature': 20.87, 'humidity': 82.00,
            'ph': 6.50, 'rainfall': 202.93, 'ndvi': 0.65
        }
        
        prediction = model.predict(test_input)
        
        # Check prediction structure
        assert isinstance(prediction, dict)
        assert 'crop' in prediction
        assert 'confidence' in prediction
        assert 'all_probabilities' in prediction
        
        # Check prediction values
        assert isinstance(prediction['crop'], str)
        assert 0 <= prediction['confidence'] <= 1
        assert isinstance(prediction['all_probabilities'], dict)
        
        # Check that probabilities sum to approximately 1
        prob_sum = sum(prediction['all_probabilities'].values())
        assert abs(prob_sum - 1.0) < 0.01
    
    def test_model_prediction_multiple(self, model, sample_data):
        """Test model prediction with multiple inputs"""
        # Train the model first
        model.train(test_size=0.3, random_state=42)
        
        # Test multiple predictions
        test_inputs = pd.DataFrame([
            {'N': 90, 'P': 42, 'K': 43, 'temperature': 20.87, 'humidity': 82.00, 'ph': 6.50, 'rainfall': 202.93, 'ndvi': 0.65},
            {'N': 120, 'P': 60, 'K': 80, 'temperature': 25.5, 'humidity': 70.0, 'ph': 7.0, 'rainfall': 150.0, 'ndvi': 0.75}
        ])
        
        predictions = model.predict(test_inputs)
        
        # Check predictions structure
        assert isinstance(predictions, list)
        assert len(predictions) == 2
        
        for prediction in predictions:
            assert isinstance(prediction, dict)
            assert 'crop' in prediction
            assert 'confidence' in prediction
            assert 'all_probabilities' in prediction
    
    def test_model_save_load(self, model, sample_data, temp_model_path):
        """Test model saving and loading"""
        # Set temporary model path
        model.model_path = temp_model_path
        
        # Train the model
        model.train(test_size=0.3, random_state=42)
        
        # Save the model
        model.save_model()
        assert temp_model_path.exists()
        
        # Create new model instance and load
        new_model = CropModel()
        new_model.model_path = temp_model_path
        success = new_model.load_model()
        
        assert success is True
        assert new_model.model is not None
        
        # Test that loaded model produces same predictions
        test_input = {
            'N': 90, 'P': 42, 'K': 43,
            'temperature': 20.87, 'humidity': 82.00,
            'ph': 6.50, 'rainfall': 202.93, 'ndvi': 0.65
        }
        
        original_prediction = model.predict(test_input)
        loaded_prediction = new_model.predict(test_input)
        
        assert original_prediction['crop'] == loaded_prediction['crop']
        assert abs(original_prediction['confidence'] - loaded_prediction['confidence']) < 0.001
    
    def test_model_info(self, model, sample_data):
        """Test model information retrieval"""
        # Initially should return None
        info = model.get_model_info()
        assert info is None
        
        # Train the model
        model.train(test_size=0.3, random_state=42)
        
        # Now should return info
        info = model.get_model_info()
        assert isinstance(info, dict)
        assert 'model_type' in info
        assert 'n_features' in info
        assert 'feature_columns' in info
        assert 'n_classes' in info
        assert 'classes' in info
        
        assert info['model_type'] == 'RandomForestClassifier'
        assert info['n_features'] > 0
        assert isinstance(info['feature_columns'], list)
        assert info['n_classes'] > 0
        assert isinstance(info['classes'], list)
    
    def test_model_prediction_missing_features(self, model, sample_data):
        """Test model prediction with missing features"""
        # Train the model first
        model.train(test_size=0.3, random_state=42)
        
        # Test with missing NDVI feature
        test_input = {
            'N': 90, 'P': 42, 'K': 43,
            'temperature': 20.87, 'humidity': 82.00,
            'ph': 6.50, 'rainfall': 202.93
            # Missing 'ndvi'
        }
        
        # Should still work (missing features should be filled with defaults)
        prediction = model.predict(test_input)
        assert 'crop' in prediction
        assert 'confidence' in prediction
    
    def test_model_prediction_without_training(self, model):
        """Test prediction without training (should fail)"""
        test_input = {
            'N': 90, 'P': 42, 'K': 43,
            'temperature': 20.87, 'humidity': 82.00,
            'ph': 6.50, 'rainfall': 202.93, 'ndvi': 0.65
        }
        
        with pytest.raises(ValueError, match="Model not trained or loaded"):
            model.predict(test_input)

class TestModelUtilities:
    """Test model utility functions"""
    
    def test_create_sample_data(self):
        """Test sample data creation"""
        df = create_sample_data()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        
        expected_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
        assert all(col in df.columns for col in expected_columns)
        
        # Check data ranges
        assert df['N'].min() >= 0
        assert df['P'].min() >= 0
        assert df['K'].min() >= 0
        assert df['humidity'].min() >= 0
        assert df['humidity'].max() <= 100
        assert df['ph'].min() >= 0
        assert df['ph'].max() <= 14
    
    def test_prepare_features_target(self):
        """Test feature and target preparation"""
        df = create_sample_data()
        X, y = prepare_features_target(df)
        
        assert isinstance(X, pd.DataFrame)
        assert len(X) == len(y)
        assert len(X.columns) >= 7  # At least the basic features
        
        # Check that all features are numeric
        assert X.dtypes.apply(lambda x: pd.api.types.is_numeric_dtype(x)).all()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])