import random
from datetime import datetime
from db.combined_database import PlantDatabase


class PlantModel:
    '''Klasa rosliny, przechowuje stan i logike'''
    def __init__(self):
        '''self odnosi się do bierzącej instancji klasy, czyli obiektu, "_" oznacza prywatny'''
        self._moisture=0
        self._light=0
        self._temperature=0
        self._time_of_day=0
        self._message="Moja apka roślinki"
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
        """Symuluje nowe odczyty z czujników"""
        self._moisture = random.randint(10, 90)
        self._light = random.randint(20, 100)
        self._temperature = random.randint(15, 30)
        self._time_of_day = random.randint(0, 23)
        
        # Zapisz odczyt do bazy danych
        self.database.save_reading(self._moisture, self._light, self._temperature, self._time_of_day)