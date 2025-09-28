import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from pathlib import Path
from loguru import logger
from .config import settings
from .preprocessing import load_and_clean_data, prepare_features_target

class CropModel:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'ndvi']
        self.model_path = Path(settings.MODEL_PATH)
        
    def train(self, test_size=0.2, random_state=42):
        """Train the crop recommendation model"""
        logger.info("Starting model training")
        
        # Load and prepare data
        df = load_and_clean_data()
        X, y = prepare_features_target(df)
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
        )
        
        logger.info(f"Training set size: {len(X_train)}")
        logger.info(f"Test set size: {len(X_test)}")
        
        # Initialize and train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=random_state,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        logger.info(f"Training accuracy: {train_score:.4f}")
        logger.info(f"Test accuracy: {test_score:.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X, y_encoded, cv=5)
        logger.info(f"Cross-validation scores: {cv_scores}")
        logger.info(f"Mean CV score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Generate predictions for classification report
        y_pred = self.model.predict(X_test)
        
        # Convert back to original labels for report
        y_test_original = self.label_encoder.inverse_transform(y_test)
        y_pred_original = self.label_encoder.inverse_transform(y_pred)
        
        logger.info("Classification Report:")
        logger.info(f"\n{classification_report(y_test_original, y_pred_original)}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info("Feature Importance:")
        logger.info(f"\n{feature_importance}")
        
        # Save model
        self.save_model()
        
        return {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': feature_importance.to_dict('records')
        }
    
    def predict(self, input_data):
        """Make predictions for new data"""
        if self.model is None:
            self.load_model()
        
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Prepare input data
        if isinstance(input_data, dict):
            # Convert dict to DataFrame
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data
        
        # Ensure all required features are present
        missing_features = set(self.feature_columns) - set(input_df.columns)
        if missing_features:
            logger.warning(f"Missing features: {missing_features}")
            # Fill missing features with default values
            for feature in missing_features:
                if feature == 'ndvi':
                    input_df[feature] = 0.5  # Default NDVI value
                else:
                    input_df[feature] = 0
        
        # Select and order features correctly
        input_features = input_df[self.feature_columns]
        
        # Make prediction
        prediction_encoded = self.model.predict(input_features)
        prediction_proba = self.model.predict_proba(input_features)
        
        # Convert back to original labels
        prediction = self.label_encoder.inverse_transform(prediction_encoded)
        
        # Get confidence (max probability)
        confidence = np.max(prediction_proba, axis=1)
        
        if len(prediction) == 1:
            return {
                'crop': prediction[0],
                'confidence': float(confidence[0]),
                'all_probabilities': {
                    crop: float(prob) for crop, prob in zip(
                        self.label_encoder.classes_,
                        prediction_proba[0]
                    )
                }
            }
        else:
            return [
                {
                    'crop': pred,
                    'confidence': float(conf),
                    'all_probabilities': {
                        crop: float(prob) for crop, prob in zip(
                            self.label_encoder.classes_,
                            proba
                        )
                    }
                }
                for pred, conf, proba in zip(prediction, confidence, prediction_proba)
            ]
    
    def save_model(self):
        """Save the trained model and label encoder"""
        # Create model directory if it doesn't exist
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'feature_columns': self.feature_columns
        }
        
        joblib.dump(model_data, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a trained model"""
        if not self.model_path.exists():
            logger.error(f"Model file not found at {self.model_path}")
            return False
        
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.label_encoder = model_data['label_encoder']
            self.feature_columns = model_data.get('feature_columns', self.feature_columns)
            logger.info(f"Model loaded from {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def get_model_info(self):
        """Get information about the trained model"""
        if self.model is None:
            return None
        
        return {
            'model_type': type(self.model).__name__,
            'n_features': len(self.feature_columns),
            'feature_columns': self.feature_columns,
            'n_classes': len(self.label_encoder.classes_),
            'classes': self.label_encoder.classes_.tolist()
        }