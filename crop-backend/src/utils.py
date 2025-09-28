import os
import requests
import zipfile
from pathlib import Path
from loguru import logger
from .config import settings

def setup_kaggle_credentials():
    """Set up Kaggle API credentials"""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    
    credentials_file = kaggle_dir / 'kaggle.json'
    
    if not credentials_file.exists():
        credentials = {
            "username": settings.KAGGLE_USERNAME,
            "key": settings.KAGGLE_KEY
        }
        
        if credentials["username"] and credentials["key"]:
            import json
            with open(credentials_file, 'w') as f:
                json.dump(credentials, f)
            
            # Set proper permissions
            os.chmod(credentials_file, 0o600)
            logger.info("Kaggle credentials set up successfully")
            return True
        else:
            logger.error("Kaggle credentials not provided in environment variables")
            return False
    else:
        logger.info("Kaggle credentials already exist")
        return True

def download_kaggle_dataset(dataset_id, download_path=None):
    """Download dataset from Kaggle"""
    if not setup_kaggle_credentials():
        logger.error("Failed to set up Kaggle credentials")
        return False
    
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        if download_path is None:
            download_path = settings.DATA_DIR
        
        download_path = Path(download_path)
        download_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Downloading dataset {dataset_id} to {download_path}")
        api.dataset_download_files(dataset_id, path=download_path, unzip=True)
        
        logger.info(f"Successfully downloaded dataset {dataset_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to download dataset {dataset_id}: {e}")
        return False

def download_crop_datasets():
    """Download required crop datasets"""
    datasets = [
        "atharvaingle/crop-recommendation-dataset",
        # Note: The second dataset URL appears to be a Kaggle notebook, not a dataset
        # We'll handle it separately or create equivalent functionality
    ]
    
    success_count = 0
    for dataset in datasets:
        if download_kaggle_dataset(dataset):
            success_count += 1
    
    logger.info(f"Downloaded {success_count}/{len(datasets)} datasets successfully")
    return success_count == len(datasets)

def validate_input_data(data):
    """Validate crop prediction input data"""
    required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    optional_fields = ['ndvi']
    
    errors = []
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(data[field], (int, float)):
            errors.append(f"Field {field} must be a number")
    
    # Validate ranges if data is present
    if 'N' in data and (data['N'] < 0 or data['N'] > 200):
        errors.append("Nitrogen (N) should be between 0-200")
    
    if 'P' in data and (data['P'] < 0 or data['P'] > 200):
        errors.append("Phosphorus (P) should be between 0-200")
    
    if 'K' in data and (data['K'] < 0 or data['K'] > 300):
        errors.append("Potassium (K) should be between 0-300")
    
    if 'temperature' in data and (data['temperature'] < -50 or data['temperature'] > 60):
        errors.append("Temperature should be between -50°C to 60°C")
    
    if 'humidity' in data and (data['humidity'] < 0 or data['humidity'] > 100):
        errors.append("Humidity should be between 0-100%")
    
    if 'ph' in data and (data['ph'] < 0 or data['ph'] > 14):
        errors.append("pH should be between 0-14")
    
    if 'rainfall' in data and data['rainfall'] < 0:
        errors.append("Rainfall should be non-negative")
    
    if 'ndvi' in data and data['ndvi'] is not None and (data['ndvi'] < -1 or data['ndvi'] > 1):
        errors.append("NDVI should be between -1 and 1")
    
    return errors

def setup_logging():
    """Set up logging configuration"""
    from loguru import logger
    
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Add file handler
    log_file = settings.LOG_DIR / "crop_backend.log"
    settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        sink=log_file,
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )
    
    logger.info("Logging setup completed")

def get_crop_info(crop_name):
    """Get additional information about a recommended crop"""
    crop_info = {
        'rice': {
            'season': 'Kharif',
            'water_requirement': 'High',
            'soil_type': 'Clay, Clay Loam',
            'temperature_range': '20-37°C',
            'rainfall_range': '100-200cm',
            'growth_period': '120-150 days'
        },
        'wheat': {
            'season': 'Rabi',
            'water_requirement': 'Medium',
            'soil_type': 'Clay Loam, Sandy Loam',
            'temperature_range': '10-25°C',
            'rainfall_range': '30-100cm',
            'growth_period': '120-150 days'
        },
        'corn': {
            'season': 'Kharif',
            'water_requirement': 'Medium-High',
            'soil_type': 'Well-drained Loamy',
            'temperature_range': '18-27°C',
            'rainfall_range': '50-100cm',
            'growth_period': '80-120 days'
        },
        'cotton': {
            'season': 'Kharif',
            'water_requirement': 'Medium',
            'soil_type': 'Black Cotton Soil',
            'temperature_range': '21-30°C',
            'rainfall_range': '50-100cm',
            'growth_period': '180-200 days'
        }
    }
    
    return crop_info.get(crop_name.lower(), {
        'season': 'Not specified',
        'water_requirement': 'Not specified',
        'soil_type': 'Not specified',
        'temperature_range': 'Not specified',
        'rainfall_range': 'Not specified',
        'growth_period': 'Not specified'
    })

def create_directory_structure():
    """Create necessary directory structure"""
    directories = [
        settings.DATA_DIR,
        settings.MODEL_DIR,
        settings.LOG_DIR,
        Path(settings.BASE_DIR) / "notebooks",
        Path(settings.BASE_DIR) / "tests"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

if __name__ == "__main__":
    setup_logging()
    create_directory_structure()
    download_crop_datasets()