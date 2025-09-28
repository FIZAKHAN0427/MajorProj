import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
from .config import settings

def load_and_clean_data():
    """Load and preprocess Kaggle datasets"""
    logger.info("Loading and cleaning crop recommendation data")
    
    data_dir = Path(settings.DATA_PATH)
    
    # Load primary crop recommendation dataset
    crop_data_path = data_dir / "Crop_recommendation.csv"
    if crop_data_path.exists():
        df = pd.read_csv(crop_data_path)
        logger.info(f"Loaded crop recommendation dataset with {len(df)} rows")
    else:
        logger.warning("Crop recommendation dataset not found, creating sample data")
        # Create sample data if dataset not available
        df = create_sample_data()
    
    # Basic preprocessing
    df = clean_data(df)
    
    # Load Indian crops dataset if available
    indian_crops_path = data_dir / "indian_crops.csv"
    if indian_crops_path.exists():
        indian_df = pd.read_csv(indian_crops_path)
        logger.info(f"Loaded Indian crops dataset with {len(indian_df)} rows")
        # Merge or combine datasets as needed
        df = combine_datasets(df, indian_df)
    
    # Load Sentinel NDVI data if available
    sentinel_path = data_dir / "sentinel_ndvi.csv"
    if sentinel_path.exists():
        sentinel_df = pd.read_csv(sentinel_path)
        logger.info(f"Loaded Sentinel NDVI data with {len(sentinel_df)} rows")
        df = add_sentinel_features(df, sentinel_df)
    
    logger.info(f"Final processed dataset has {len(df)} rows and {len(df.columns)} columns")
    return df

def clean_data(df):
    """Clean and validate the dataset"""
    logger.info("Cleaning dataset")
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {initial_rows - len(df)} duplicate rows")
    
    # Handle missing values
    df = df.dropna()
    
    # Validate data ranges
    if 'ph' in df.columns:
        df = df[(df['ph'] >= 0) & (df['ph'] <= 14)]
    if 'temperature' in df.columns:
        df = df[(df['temperature'] >= -50) & (df['temperature'] <= 60)]
    if 'humidity' in df.columns:
        df = df[(df['humidity'] >= 0) & (df['humidity'] <= 100)]
    
    return df

def create_sample_data():
    """Create sample data for testing"""
    logger.info("Creating sample crop recommendation data")
    
    np.random.seed(42)
    n_samples = 1000
    
    crops = ['rice', 'wheat', 'corn', 'cotton', 'sugarcane', 'jute', 'coconut', 'papaya', 'orange', 'apple']
    
    data = {
        'N': np.random.randint(0, 150, n_samples),
        'P': np.random.randint(0, 150, n_samples),
        'K': np.random.randint(0, 210, n_samples),
        'temperature': np.random.uniform(8, 45, n_samples),
        'humidity': np.random.uniform(14, 100, n_samples),
        'ph': np.random.uniform(3.5, 10, n_samples),
        'rainfall': np.random.uniform(20, 300, n_samples),
        'label': np.random.choice(crops, n_samples)
    }
    
    return pd.DataFrame(data)

def combine_datasets(df1, df2):
    """Combine multiple crop datasets"""
    logger.info("Combining datasets")
    # Simple concatenation - can be made more sophisticated
    combined = pd.concat([df1, df2], ignore_index=True)
    return combined

def add_sentinel_features(df, sentinel_df):
    """Add Sentinel satellite features to the dataset"""
    logger.info("Adding Sentinel NDVI features")
    
    # If NDVI column doesn't exist, add random NDVI values for demonstration
    if 'ndvi' not in df.columns:
        df['ndvi'] = np.random.uniform(0.1, 0.9, len(df))
    
    return df

def prepare_features_target(df, target_column='label'):
    """Prepare features and target for model training"""
    logger.info("Preparing features and target variables")
    
    # Define feature columns
    feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Add NDVI if available
    if 'ndvi' in df.columns:
        feature_columns.append('ndvi')
    
    X = df[feature_columns]
    y = df[target_column]
    
    logger.info(f"Features: {feature_columns}")
    logger.info(f"Target classes: {y.unique().tolist()}")
    
    return X, y