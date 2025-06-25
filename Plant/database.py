import sqlite3
import os
from datetime import datetime
from typing import List, Tuple


class PlantDatabase:
    """Klasa do zarządzania bazą danych z danymi roślinki"""
    
    def __init__(self, db_path: str = "plant_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicjalizuje bazę danych i tworzy tabelę jeśli nie istnieje"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
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