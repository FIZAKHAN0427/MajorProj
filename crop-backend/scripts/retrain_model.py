#!/usr/bin/env python3
"""
Script to retrain the crop recommendation model
"""

import sys
import argparse
from pathlib import Path
from loguru import logger

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.model import CropModel
from src.utils import setup_logging, download_crop_datasets
from src.config import settings

def main():
    """Main function to retrain the model"""
    parser = argparse.ArgumentParser(description="Retrain crop recommendation model")
    parser.add_argument("--download-data", action="store_true", help="Download datasets from Kaggle")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set size (default: 0.2)")
    parser.add_argument("--random-state", type=int, default=42, help="Random state for reproducibility")
    parser.add_argument("--force", action="store_true", help="Force retrain even if model exists")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger.info("Starting model retraining")
    
    # Check if model already exists
    model_path = Path(settings.MODEL_PATH)
    if model_path.exists() and not args.force:
        logger.warning(f"Model already exists at {model_path}")
        logger.info("Use --force flag to retrain anyway")
        response = input("Do you want to retrain anyway? (y/N): ")
        if response.lower() != 'y':
            logger.info("Training cancelled")
            return 0
    
    try:
        # Download datasets if requested
        if args.download_data:
            logger.info("Downloading crop datasets...")
            success = download_crop_datasets()
            if not success:
                logger.warning("Failed to download some datasets, continuing with existing data")
        
        # Initialize model
        logger.info("Initializing crop model")
        model = CropModel()
        
        # Train model
        logger.info("Starting model training...")
        training_results = model.train(
            test_size=args.test_size,
            random_state=args.random_state
        )
        
        # Display training results
        logger.info("Training completed successfully!")
        logger.info("Training Results:")
        logger.info(f"  Training Accuracy: {training_results['train_accuracy']:.4f}")
        logger.info(f"  Test Accuracy: {training_results['test_accuracy']:.4f}")
        logger.info(f"  Cross-validation Mean: {training_results['cv_mean']:.4f}")
        logger.info(f"  Cross-validation Std: {training_results['cv_std']:.4f}")
        
        logger.info("Feature Importance:")
        for feature_info in training_results['feature_importance'][:5]:  # Top 5 features
            logger.info(f"  {feature_info['feature']}: {feature_info['importance']:.4f}")
        
        # Test the model with sample prediction
        logger.info("Testing model with sample prediction...")
        sample_data = {
            'N': 90, 'P': 42, 'K': 43,
            'temperature': 20.87, 'humidity': 82.00,
            'ph': 6.50, 'rainfall': 202.93, 'ndvi': 0.65
        }
        
        prediction = model.predict(sample_data)
        logger.info(f"Sample prediction: {prediction['crop']} (confidence: {prediction['confidence']:.3f})")
        
        logger.info(f"Model saved to: {settings.MODEL_PATH}")
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1
    
    logger.info("Model retraining completed successfully")
    return 0

if __name__ == "__main__":
    exit(main())