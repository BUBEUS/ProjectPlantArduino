import sqlite3
import os
from datetime import datetime
from typing import List, Tuple


class PlantDatabase:
    """Klasa do zarządzania bazą danych z danymi roślinki i pogody"""
    
    def __init__(self, db_path: str = "data/plant_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicjalizuje bazę danych i tworzy tabele jeśli nie istnieją"""
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Plant sensor readings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    moisture INTEGER NOT NULL,
                    light INTEGER NOT NULL,
                    temperature INTEGER NOT NULL,
                    time_of_day INTEGER NOT NULL
                )
            ''')
            
            # Weather data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    time TEXT,
                    temperature REAL,
                    humidity REAL,
                    pressure REAL,
                    wind_speed REAL,
                    wind_direction REAL,
                    precipitation REAL,
                    visibility REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date, time)
                )
            ''')
            
            conn.commit()
    
    def save_reading(self, moisture: int, light: int, temperature: int, time_of_day: int):
        """Zapisuje odczyt czujników do bazy danych"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sensor_readings (timestamp, moisture, light, temperature, time_of_day)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, moisture, light, temperature, time_of_day))
            conn.commit()
    
    def get_all_readings(self) -> List[Tuple]:
        """Pobiera wszystkie odczyty z bazy danych"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, moisture, light, temperature, time_of_day
                FROM sensor_readings
                ORDER BY timestamp DESC
            ''')
            return cursor.fetchall()
    
    def get_recent_readings(self, limit: int = 100) -> List[Tuple]:
        """Pobiera ostatnie N odczytów z bazy danych"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, moisture, light, temperature, time_of_day
                FROM sensor_readings
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
    
    def clear_database(self):
        """Czyści wszystkie dane z bazy danych"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sensor_readings')
            conn.commit()
    
    def get_database_stats(self) -> dict:
        """Zwraca statystyki bazy danych"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM sensor_readings')
            total_records = cursor.fetchone()[0]
            
            if total_records > 0:
                cursor.execute('''
                    SELECT MIN(timestamp), MAX(timestamp)
                    FROM sensor_readings
                ''')
                min_date, max_date = cursor.fetchone()
                
                cursor.execute('''
                    SELECT AVG(moisture), AVG(light), AVG(temperature)
                    FROM sensor_readings
                ''')
                avg_moisture, avg_light, avg_temp = cursor.fetchone()
                
                return {
                    'total_records': total_records,
                    'date_range': (min_date, max_date),
                    'averages': {
                        'moisture': round(avg_moisture, 1) if avg_moisture else 0,
                        'light': round(avg_light, 1) if avg_light else 0,
                        'temperature': round(avg_temp, 1) if avg_temp else 0
                    }
                }
            else:
                return {
                    'total_records': 0,
                    'date_range': (None, None),
                    'averages': {'moisture': 0, 'light': 0, 'temperature': 0}
                }
    
    # Weather data methods
    def store_weather_data(self, records):
        """Store weather data in SQLite database, preventing duplicates"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                new_records_count = 0
                duplicate_count = 0
                
                for record in records:
                    # Check if record already exists
                    cursor.execute('''
                        SELECT COUNT(*) FROM weather_data 
                        WHERE date = ? AND time = ?
                    ''', (record['date'], record['time']))
                    
                    exists = cursor.fetchone()[0] > 0
                    
                    if not exists:
                        cursor.execute('''
                            INSERT INTO weather_data 
                            (date, time, temperature, humidity, pressure, wind_speed, 
                             wind_direction, precipitation, visibility)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            record['date'],
                            record['time'],
                            record.get('temp'),
                            record.get('rhum'),
                            record.get('pres'),
                            record.get('wspd'),
                            record.get('wdir'),
                            record.get('prcp'),
                            record.get('visibility')
                        ))
                        new_records_count += 1
                    else:
                        duplicate_count += 1
                
                conn.commit()
                return new_records_count, duplicate_count
                
        except Exception as e:
            raise Exception(f"Error storing weather data: {e}")
    
    def get_latest_weather_record_datetime(self):
        """Get the datetime of the most recent weather record in the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT date, time FROM weather_data 
                    ORDER BY date DESC, time DESC 
                    LIMIT 1
                ''')
                
                row = cursor.fetchone()
                
                if row:
                    # Combine date and time strings back to datetime
                    date_str, time_str = row
                    datetime_str = f"{date_str} {time_str}"
                    return datetime.fromisoformat(datetime_str)
                else:
                    return None
                    
        except Exception as e:
            raise Exception(f"Error getting latest weather record datetime: {e}")
    
    def get_latest_weather_data(self, limit: int = 10):
        """Retrieve latest weather data from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM weather_data 
                    ORDER BY date DESC, time DESC 
                    LIMIT ?
                ''', (limit,))
                
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                result = []
                for row in rows:
                    record = dict(zip(columns, row))
                    result.append(record)
                
                return result
                
        except Exception as e:
            raise Exception(f"Error retrieving weather data: {e}")