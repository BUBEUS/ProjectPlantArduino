#!/usr/bin/env python3
"""
Weather Data Collector for Bydgoszcz using Open-Meteo API
Collects hourly weather data and stores it in SQLite database
"""

from datetime import datetime, timedelta
import requests
import pandas as pd
import logging
from .config import BYDGOSZCZ_LAT, BYDGOSZCZ_LON

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weather_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WeatherCollector:
    def __init__(self, database=None):
        """Initialize the weather collector with database instance"""
        self.database = database
        # Bydgoszcz coordinates
        self.latitude = BYDGOSZCZ_LAT
        self.longitude = BYDGOSZCZ_LON
    
    def collect_data_range(self, start_time: datetime, end_time: datetime):
        """Collect weather data for a specific date range"""
        try:
            logger.info(f"Collecting data from {start_time} to {end_time}")
            
            # Calculate the number of days needed for the API call
            days_diff = (end_time - start_time).days + 1
            past_days = min(days_diff, 92)  # Open-Meteo historical limit is ~3 months
            
            # Fetch hourly data from Open-Meteo API
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "hourly": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m,precipitation,visibility",
                "past_days": past_days,
                "forecast_days": 1,
                "timezone": "Europe/Warsaw"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'hourly' not in data:
                logger.warning("No hourly data received from Open-Meteo")
                return
            
            # Convert to pandas DataFrame
            hourly_data = data['hourly']
            df = pd.DataFrame({
                'time': pd.to_datetime(hourly_data['time']),
                'temp': hourly_data['temperature_2m'],
                'rhum': hourly_data['relative_humidity_2m'],
                'pres': hourly_data['surface_pressure'],
                'wspd': hourly_data['wind_speed_10m'],
                'wdir': hourly_data['wind_direction_10m'],
                'prcp': hourly_data['precipitation'],
                'visibility': hourly_data['visibility']
            })
            
            # Filter data for the requested time range
            df = df[(df['time'] >= start_time) & (df['time'] <= end_time)]
            
            if df.empty:
                logger.warning("No data in requested time range")
                return
            
            # Convert DataFrame to list of dictionaries for processing
            records = []
            for _, row in df.iterrows():
                dt = row['time'].to_pydatetime()  # Convert pandas Timestamp to Python datetime
                record = {
                    'date': dt.date().isoformat(),  # Convert date to string format
                    'time': dt.time().isoformat(),  # Convert time to string format
                    'temp': row['temp'],
                    'rhum': row['rhum'],
                    'pres': row['pres'],
                    'wspd': row['wspd'],
                    'wdir': row['wdir'],
                    'prcp': row['prcp'],
                    'visibility': row['visibility']
                }
                records.append(record)
            
            # Store data in database
            if self.database:
                new_count, duplicate_count = self.database.store_weather_data(records)
                logger.info(f"Successfully collected and stored {new_count} new records, skipped {duplicate_count} duplicates for date range")
            else:
                logger.error("No database instance provided")
            
        except Exception as e:
            logger.error(f"Error collecting weather data for range: {e}")
    
    def collect_hourly_data(self, hours_back: int = 1):
        """Collect weather data for the last specified hours"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)
        self.collect_data_range(start_time, end_time)
    

    
    def collect_missing_data(self):
        """Collect any missing data since the last record"""
        try:
            if not self.database:
                logger.error("No database instance provided")
                return
                
            latest_record_time = self.database.get_latest_weather_record_datetime()
            current_time = datetime.now()
            
            if latest_record_time is None:
                # No records exist, collect last 7 days
                logger.info("No existing weather records found. Collecting last 7 days of data.")
                start_time = current_time - timedelta(days=7)
                self.collect_data_range(start_time, current_time)
            else:
                # Calculate time gap
                time_gap = current_time - latest_record_time
                
                if time_gap > timedelta(hours=2):  # More than 2 hours gap
                    logger.info(f"Found weather data gap of {time_gap}. Latest record: {latest_record_time}")
                    # Start from the hour after the latest record
                    start_time = latest_record_time + timedelta(hours=1)
                    # Round down to the nearest hour
                    start_time = start_time.replace(minute=0, second=0, microsecond=0)
                    self.collect_data_range(start_time, current_time)
                else:
                    logger.info("No significant weather data gap found. Database is up to date.")
                    
        except Exception as e:
            logger.error(f"Error collecting missing weather data: {e}")
    
