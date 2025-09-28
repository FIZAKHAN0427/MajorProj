import ee
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from loguru import logger
from .config import settings

class SentinelDataFetcher:
    def __init__(self):
        self.authenticated = False
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Earth Engine"""
        try:
            if settings.GOOGLE_APPLICATION_CREDENTIALS:
                # Authenticate using service account
                credentials = ee.ServiceAccountCredentials(
                    email=None,  # Will be read from service account file
                    key_file=settings.GOOGLE_APPLICATION_CREDENTIALS
                )
                ee.Initialize(credentials)
            else:
                # Try to use cached credentials
                ee.Initialize()
            
            self.authenticated = True
            logger.info("Successfully authenticated with Google Earth Engine")
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Earth Engine: {e}")
            logger.info("Run 'earthengine authenticate' to set up authentication")
            self.authenticated = False
    
    def fetch_ndvi_for_region(self, geometry, start_date=None, end_date=None):
        """Fetch NDVI data for a specific region"""
        if not self.authenticated:
            logger.error("Google Earth Engine not authenticated")
            return None
        
        try:
            # Default to last 30 days if dates not provided
            if not end_date:
                end_date = datetime.now()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            # Convert to string format
            start_str = start_date.strftime('%Y-%m-%d')
            end_str = end_date.strftime('%Y-%m-%d')
            
            # Load Sentinel-2 collection
            collection = ee.ImageCollection('COPERNICUS/S2_SR') \
                .filterDate(start_str, end_str) \
                .filterBounds(geometry) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
            
            # Calculate NDVI
            def calculate_ndvi(image):
                ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
                return image.addBands(ndvi)
            
            # Apply NDVI calculation
            ndvi_collection = collection.map(calculate_ndvi)
            
            # Get median NDVI
            median_ndvi = ndvi_collection.select('NDVI').median()
            
            # Sample the region
            sample = median_ndvi.sample(
                region=geometry,
                scale=10,  # 10m resolution
                numPixels=100
            ).getInfo()
            
            # Convert to DataFrame
            ndvi_data = []
            for feature in sample['features']:
                properties = feature['properties']
                coordinates = feature['geometry']['coordinates']
                ndvi_data.append({
                    'longitude': coordinates[0],
                    'latitude': coordinates[1],
                    'ndvi': properties.get('NDVI', np.nan),
                    'date': end_str
                })
            
            df = pd.DataFrame(ndvi_data)
            logger.info(f"Fetched NDVI data for {len(df)} points")
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch NDVI data: {e}")
            return None
    
    def fetch_ndvi_for_coordinates(self, lat, lon, buffer_km=1):
        """Fetch NDVI data for specific coordinates with buffer"""
        if not self.authenticated:
            logger.warning("Google Earth Engine not authenticated, returning mock data")
            return self._generate_mock_ndvi_data(lat, lon)
        
        try:
            # Create geometry
            point = ee.Geometry.Point([lon, lat])
            geometry = point.buffer(buffer_km * 1000)  # Convert km to meters
            
            return self.fetch_ndvi_for_region(geometry)
            
        except Exception as e:
            logger.error(f"Failed to fetch NDVI for coordinates {lat}, {lon}: {e}")
            return self._generate_mock_ndvi_data(lat, lon)
    
    def _generate_mock_ndvi_data(self, lat, lon):
        """Generate mock NDVI data when Earth Engine is not available"""
        logger.info("Generating mock NDVI data")
        
        # Generate realistic NDVI values based on location
        # Higher NDVI for tropical regions, lower for arid regions
        base_ndvi = 0.3 + (abs(lat) / 90) * 0.4
        
        # Add some randomness
        np.random.seed(int(lat * lon * 1000) % 2**32)
        ndvi_values = np.random.normal(base_ndvi, 0.1, 10)
        ndvi_values = np.clip(ndvi_values, 0, 1)  # NDVI range is 0-1
        
        data = []
        for i, ndvi in enumerate(ndvi_values):
            data.append({
                'longitude': lon + np.random.uniform(-0.01, 0.01),
                'latitude': lat + np.random.uniform(-0.01, 0.01),
                'ndvi': ndvi,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
        
        return pd.DataFrame(data)
    
    def get_regional_ndvi_summary(self, region_name, bbox=None):
        """Get NDVI summary for a named region"""
        # Pre-defined bounding boxes for major Indian agricultural regions
        indian_regions = {
            'punjab': [74.0, 29.5, 76.5, 32.5],
            'haryana': [74.0, 27.5, 77.5, 30.5],
            'uttar_pradesh': [77.0, 24.0, 84.5, 30.5],
            'madhya_pradesh': [74.0, 21.0, 82.5, 26.5],
            'bihar': [83.0, 24.5, 88.5, 27.5],
            'west_bengal': [85.0, 21.5, 89.5, 27.5],
            'maharashtra': [72.5, 15.5, 80.5, 22.0],
            'karnataka': [74.0, 11.5, 78.5, 18.5],
            'andhra_pradesh': [76.5, 12.5, 84.5, 19.5],
            'tamil_nadu': [76.0, 8.0, 80.5, 13.5]
        }
        
        if region_name.lower() in indian_regions:
            bbox = indian_regions[region_name.lower()]
        elif bbox is None:
            logger.error(f"Region {region_name} not found and no bbox provided")
            return None
        
        # Create geometry from bounding box
        geometry = ee.Geometry.Rectangle(bbox)
        
        return self.fetch_ndvi_for_region(geometry)