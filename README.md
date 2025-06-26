# Plant Monitoring System

A comprehensive plant monitoring system that combines plant sensor data collection with weather data monitoring for Bydgoszcz, Poland.
---
![image](https://github.com/user-attachments/assets/1646f752-af92-45c9-b683-522f2a6fd44c)
---

## Project goal

The final aim of the project is to create a simple application that assists in taking care of a potted plant. The interface should display conditions such as soil moisture, sunlight exposure percentage, and ambient temperature. Data will be collected and transmitted via Arduino, as well as gathered from other available sources (e.g., Meteostat). The collected data will be analyzed and presented in the form of graphs. In the future, a virtual assistant may be added to help with plant care.

## Project Structure

```
project_root/
│
├── meteo_data/                  # Weather-related functionality
│   ├── __init__.py
│   ├── config.py                # Weather data configuration
│   ├── delete_records.py       # Weather database cleanup
│   ├── sweep.md                # Weather module documentation
│   └── weather_collector.py    # Weather data collection
│
├── plant/                       # Plant monitoring functionality
│   ├── __init__.py
│   ├── analytics_window.py     # Analytics GUI window
│   ├── controller.py           # Main application controller
│   ├── model.py                # Plant data model
│   └── view.py                 # Main GUI interface
│
├── db/                          # Shared database access layer
│   ├── __init__.py
│   └── combined_database.py    # Plant database operations
│
├── data/                        # Data storage directory
│   ├── plant_data.db           # Plant sensor data (created automatically)
│   └── weather_data.db         # Weather data (created automatically)
│
├── main.py                      # Main application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Features

### 🌱 Plant Monitoring

- Real-time plant sensor simulation (moisture, light, temperature)
- Modern GUI with status indicators and controls
- Historical data storage and analytics
- Data visualization with sortable tables
- Database management (clear, statistics)

### ☀️ Weather Data Collection

- Automatic weather data collection for Bydgoszcz, Poland
- Uses Open-Meteo API (no API key required)
- Hourly data collection with gap detection
- Continuous or one-time collection modes
- Data cleanup and management tools

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ProjektKwiatArduinoS
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 🌿 Plant Monitoring

Run the plant monitoring GUI & Weather Collector:

```bash
python main.py
```

Note: If there is no weather data, collector will gather data from last 7 days.

### 🧹 Weather Data Management

Delete all weather records:

```bash
python -m meteo_data.delete_records
```

Check weather database contents:

```bash
sqlite3 data/plant_data.db "SELECT * FROM weather_data ORDER BY date DESC, time DESC LIMIT 10;"
```

Or open data/plant_data.db via data browser like DB Browser

## Configuration

### Weather Data

Configuration is handled in `meteo_data/config.py`. You can create a `.env` file to override default settings:

```env
DATABASE_PATH=data/weather_data.db
LOG_LEVEL=INFO
LOG_FILE=weather_collector.log
```

### Plant Data

Plant data is automatically stored in `data/plant_data.db`. The database is created automatically when the application runs.

## Development

The project follows a modular architecture:

- `meteo_data/`: Weather data collection and management
- `plant/`: Plant monitoring GUI and logic
- `db/`: Shared database access layer
- `data/`: Data storage (databases are created automatically)

## Dependencies

- **tkinter** — GUI framework (included with Python)
- **requests** — HTTP requests for weather API
- **pandas** — Data processing and analysis
- **schedule** — Task scheduling for weather collection
- **python-dotenv** — Environment variable management
- **sqlite3** — Database (included with Python)

**Optional:**

- **matplotlib** — Enhanced data visualization
- **numpy** — Numerical computations

## Screenshots
---
![image](https://github.com/user-attachments/assets/558882c1-84bd-46c8-894d-dd3faf4258de)
---
![image](https://github.com/user-attachments/assets/736d9c15-ad76-4e12-a96b-0db1104ba761)


