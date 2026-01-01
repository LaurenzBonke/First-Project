"""
Mock temperature sensor for demonstration and testing.
In a real Raspberry Pi setup, this would interface with actual hardware like DHT22, DS18B20, etc.
"""

import random
import time
from .base_sensor import BaseSensor


class TemperatureSensor(BaseSensor):
    """
    Simulated temperature sensor.
    Generates realistic temperature readings with gradual changes.
    """
    
    def __init__(self, min_temp: float = 18.0, max_temp: float = 28.0):
        """
        Initialize temperature sensor.
        
        Args:
            min_temp: Minimum temperature value
            max_temp: Maximum temperature value
        """
        super().__init__(name="temperature", unit="°C")
        self.min_temp = min_temp
        self.max_temp = max_temp
        self._current_temp = random.uniform(min_temp, max_temp)
    
    def read(self) -> float:
        """
        Read temperature value.
        Simulates gradual temperature changes for realistic behavior.
        
        Returns:
            Temperature in Celsius
        """
        # Simulate gradual temperature change
        change = random.uniform(-0.5, 0.5)
        self._current_temp += change
        
        # Keep within bounds
        self._current_temp = max(self.min_temp, min(self.max_temp, self._current_temp))
        
        # Round to 1 decimal place
        return round(self._current_temp, 1)


class RealTemperatureSensor(BaseSensor):
    """
    Template for real temperature sensor implementation.
    Replace the read() method with actual hardware communication code.
    
    Example for DHT22 sensor:
        import Adafruit_DHT
        sensor = Adafruit_DHT.DHT22
        pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    """
    
    def __init__(self, pin: int = 4):
        super().__init__(name="temperature", unit="°C")
        self.pin = pin
        # Initialize hardware here
    
    def read(self) -> float:
        """
        Read from actual hardware sensor.
        This is a placeholder - implement actual hardware reading.
        """
        # TODO: Implement actual sensor reading
        # Example: return Adafruit_DHT.read_retry(self.sensor_type, self.pin)[1]
        raise NotImplementedError("Real sensor implementation required")
