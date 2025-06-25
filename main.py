#!/usr/bin/env python3
"""
Main entry point for the Plant Monitoring System
Combines plant monitoring and weather data collection functionality
"""

import sys
from Plant.controller import SystemController
from meteo_data.weather_collector import WeatherCollector
from db.combined_database import PlantDatabase


def main():
    """Main function to run the application"""
    print("Starting Plant Monitoring System...")
    
    # Initialize shared database
    database = PlantDatabase()
    
    # Initialize weather collector with shared database
    weather_collector = WeatherCollector(database)
    
    # Collect weather data on startup
    print("Collecting weather data...")
    try:
        weather_collector.collect_missing_data()
        weather_collector.collect_hourly_data(hours_back=1)
        
        # Show latest weather data
        latest_weather = database.get_latest_weather_data(3)
        if latest_weather and len(latest_weather) > 0:
            print(f"Latest weather data collected: {len(latest_weather)} records")
            latest = latest_weather[0]
            print(f"Most recent: {latest['date']} {latest['time']} - Temp: {latest['temperature']}°C, Humidity: {latest['humidity']}%")
        else:
            print("No weather data available")
    except Exception as e:
        print(f"Weather data collection failed: {e}")
    
    # Start the plant monitoring GUI
    print("Starting Plant Monitoring GUI...")
    app = SystemController()
    app.run()


if __name__ == "__main__":
    main()