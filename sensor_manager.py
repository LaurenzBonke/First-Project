"""
Sensor Manager - Coordinates multiple sensors and manages data collection.
This provides the modular data processing layer.
"""

from typing import List, Dict, Any
from sensors import BaseSensor


class SensorManager:
    """
    Manages multiple sensors and coordinates data collection.
    Provides a centralized interface for reading all sensor data.
    """
    
    def __init__(self):
        """Initialize the sensor manager."""
        self.sensors: List[BaseSensor] = []
    
    def add_sensor(self, sensor: BaseSensor) -> None:
        """
        Add a sensor to be managed.
        
        Args:
            sensor: Sensor instance to add
        """
        self.sensors.append(sensor)
        print(f"Added sensor: {sensor.name}")
    
    def remove_sensor(self, sensor_name: str) -> bool:
        """
        Remove a sensor by name.
        
        Args:
            sensor_name: Name of the sensor to remove
            
        Returns:
            True if sensor was removed, False if not found
        """
        for sensor in self.sensors:
            if sensor.name == sensor_name:
                self.sensors.remove(sensor)
                print(f"Removed sensor: {sensor_name}")
                return True
        return False
    
    def read_all_sensors(self) -> Dict[str, Any]:
        """
        Read data from all registered sensors.
        
        Returns:
            Dictionary with sensor data keyed by sensor name
        """
        data = {}
        for sensor in self.sensors:
            try:
                sensor_data = sensor.get_data()
                data[sensor.name] = sensor_data
            except Exception as e:
                print(f"Error reading sensor {sensor.name}: {e}")
                data[sensor.name] = {
                    'name': sensor.name,
                    'value': None,
                    'error': str(e)
                }
        return data
    
    def get_sensor(self, sensor_name: str) -> BaseSensor:
        """
        Get a specific sensor by name.
        
        Args:
            sensor_name: Name of the sensor
            
        Returns:
            Sensor instance or None if not found
        """
        for sensor in self.sensors:
            if sensor.name == sensor_name:
                return sensor
        return None
    
    def get_sensor_count(self) -> int:
        """Get the number of registered sensors."""
        return len(self.sensors)
