import random
from datetime import datetime
from db.combined_database import PlantDatabase


class PlantModel:
    '''Plant class, stores state and logic'''
    def __init__(self):
        '''self refers to the current instance of the class, i.e., the object, "_" indicates private'''
        self._moisture=0
        self._light=0
        self._temperature=0
        self._time_of_day=0
        self._message="My plant app"
        self._systemTime=""
        self.database = PlantDatabase()


    def get_moisture(self) -> int:
        return self._moisture

    def get_light(self) -> int:
        return self._light

    def get_temperature(self) -> int:
        return self._temperature

    def get_time_of_day(self) -> int:
        return self._time_of_day
    
    def get_message(self) -> str:
        return self._message
    
    def get_systemTime(self) -> datetime:
        now=datetime.now()
        self._systemTime=now
        return self._systemTime

    def get_SystemTimeSTR(self)->str:
        now=datetime.now()
        self._systemTime=now.strftime("%H:%M:%S")
        return self._systemTime
    
    def simulate_sensor_readings(self):
        """Simulates new sensor readings"""
        self._moisture = random.randint(10, 90)
        self._light = random.randint(20, 100)
        self._temperature = random.randint(15, 30)
        self._time_of_day = random.randint(0, 23)
        
        # Save reading to database
        self.database.save_reading(self._moisture, self._light, self._temperature, self._time_of_day)