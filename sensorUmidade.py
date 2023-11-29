import Adafruit_DHT
import time
 
class SensorUmidade:
    def __init__(self,DHT_PIN):
        self.DHT_PIN = DHT_PIN
        self.DHT_SENSOR = Adafruit_DHT.DHT11
    
    def readSensor(self):
        humidity, temperature = Adafruit_DHT.read(self.DHT_SENSOR, self.DHT_PIN)
        return humidity, temperature
