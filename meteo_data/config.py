"""
Configuration file for Weather Data Collector
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/weather_data.db')

# Bydgoszcz location coordinates
BYDGOSZCZ_LAT = 53.1235
BYDGOSZCZ_LON = 18.0084

# Collection settings
COLLECTION_INTERVAL_HOURS = 1
INITIAL_BACKFILL_HOURS = 24

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'weather_collector.log')

# Meteostat API settings (if needed in future)
METEOSTAT_API_KEY = os.getenv('METEOSTAT_API_KEY', None)