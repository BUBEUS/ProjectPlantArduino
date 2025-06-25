# SWEEP.md - Weather Data Collection Commands and Information

## Build/Run Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run weather collector once (test mode)
python -m meteo_data.weather_collector --once

# Run weather collector continuously (hourly collection)
python -m meteo_data.weather_collector

# Delete all records from database (interactive confirmation required)
python -m meteo_data.delete_records

# Check database contents (requires sqlite3 command line tool)
sqlite3 data/weather_data.db "SELECT * FROM weather_data ORDER BY date DESC, time DESC LIMIT 10;"
```

## Project Structure
- `weather_collector.py` - Main weather data collection script
- `delete_records.py` - Script to delete all records from database
- `config.py` - Configuration settings
- `sweep.md` - This documentation file

## Code Style Preferences
- Use type hints where appropriate
- Follow PEP 8 naming conventions
- Include comprehensive error handling and logging
- Use docstrings for classes and functions
- Prefer SQLite for simple data storage needs

## Important Notes
- The program collects weather data for Bydgoszcz, Poland (53.1235°N, 18.0084°E)
- Uses the Open-Meteo API for weather data (no API key required)
- Uses pandas for data processing instead of typing for type hints
- Data is collected hourly and stored in SQLite database in data/ directory
- Includes both one-time and continuous collection modes