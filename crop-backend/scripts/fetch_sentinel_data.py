#!/usr/bin/env python3
"""
Script to fetch Sentinel satellite data for crop recommendation
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.sentinel import SentinelDataFetcher
from src.config import settings
from src.utils import setup_logging

def main():
    """Main function to fetch Sentinel data"""
    parser = argparse.ArgumentParser(description="Fetch Sentinel NDVI data")
    parser.add_argument("--lat", type=float, default=28.6139, help="Latitude (default: Delhi)")
    parser.add_argument("--lon", type=float, default=77.2090, help="Longitude (default: Delhi)")
    parser.add_argument("--buffer-km", type=float, default=1, help="Buffer in kilometers")
    parser.add_argument("--days", type=int, default=30, help="Number of days back to fetch data")
    parser.add_argument("--output", type=str, help="Output CSV file path")
    parser.add_argument("--region", type=str, help="Predefined region name (e.g., punjab, haryana)")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger.info("Starting Sentinel data fetch")
    
    # Initialize fetcher
    fetcher = SentinelDataFetcher()
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = settings.DATA_DIR / "sentinel_ndvi.csv"
    
    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if args.region:
            # Fetch for predefined region
            logger.info(f"Fetching NDVI data for region: {args.region}")
            df = fetcher.get_regional_ndvi_summary(args.region)
        else:
            # Fetch for coordinates
            logger.info(f"Fetching NDVI data for coordinates: {args.lat}, {args.lon}")
            df = fetcher.fetch_ndvi_for_coordinates(
                lat=args.lat, 
                lon=args.lon, 
                buffer_km=args.buffer_km
            )
        
        if df is not None and not df.empty:
            # Save to CSV
            df.to_csv(output_path, index=False)
            logger.info(f"NDVI data saved to: {output_path}")
            logger.info(f"Fetched {len(df)} data points")
            
            # Display statistics
            logger.info(f"NDVI statistics:")
            logger.info(f"  Mean: {df['ndvi'].mean():.3f}")
            logger.info(f"  Min: {df['ndvi'].min():.3f}")
            logger.info(f"  Max: {df['ndvi'].max():.3f}")
            logger.info(f"  Std: {df['ndvi'].std():.3f}")
            
        else:
            logger.error("Failed to fetch NDVI data")
            return 1
            
    except Exception as e:
        logger.error(f"Error fetching Sentinel data: {e}")
        return 1
    
    logger.info("Sentinel data fetch completed successfully")
    return 0

if __name__ == "__main__":
    exit(main())