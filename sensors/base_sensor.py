"""
Base sensor class providing the interface for all sensors.
This modular design allows easy addition of new sensor types.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseSensor(ABC):
    """
    Abstract base class for all sensors.
    Each sensor must implement the read() method.
    """
    
    def __init__(self, name: str, unit: str = ""):
        """
        Initialize the sensor.
        
        Args:
            name: Sensor name/identifier
            unit: Unit of measurement (e.g., '°C', 'lux', etc.)
        """
        self.name = name
        self.unit = unit
        self._last_reading = None
    
    @abstractmethod
    def read(self) -> Any:
        """
        Read the current sensor value.
        Must be implemented by each sensor subclass.
        
        Returns:
            Current sensor reading
        """
        pass
    
    def get_data(self) -> Dict[str, Any]:
        """
        Get formatted sensor data including metadata.
        
        Returns:
            Dictionary with sensor name, value, and unit
        """
        value = self.read()
        self._last_reading = value
        return {
            'name': self.name,
            'value': value,
            'unit': self.unit
        }
    
    def get_last_reading(self) -> Any:
        """Get the last reading without triggering a new read."""
        return self._last_reading
