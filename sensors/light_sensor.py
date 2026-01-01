"""
Mock light sensor for demonstration and testing.
In a real Raspberry Pi setup, this would interface with actual hardware like BH1750, TSL2561, etc.
"""

import random
import math
import time
from .base_sensor import BaseSensor


class LightSensor(BaseSensor):
    """
    Simulated light sensor.
    Generates realistic light readings that vary throughout the day.
    """
    
    def __init__(self, min_light: float = 0, max_light: float = 1000):
        """
        Initialize light sensor.
        
        Args:
            min_light: Minimum light value in lux
            max_light: Maximum light value in lux
        """
        super().__init__(name="light", unit="lux")
        self.min_light = min_light
        self.max_light = max_light
        self._current_light = random.uniform(min_light, max_light)
    
    def read(self) -> float:
        """
        Read light intensity value.
        Simulates gradual light changes with some random variation.
        
        Returns:
            Light intensity in lux
        """
        # Simulate gradual light change
        change = random.uniform(-30, 30)
        self._current_light += change
        
        # Keep within bounds
        self._current_light = max(self.min_light, min(self.max_light, self._current_light))
        
        # Round to integer
        return round(self._current_light)


class RealLightSensor(BaseSensor):
    """
    Template for real light sensor implementation.
    Replace the read() method with actual hardware communication code.
    
    Example for BH1750 sensor:
        import smbus
        bus = smbus.SMBus(1)
        data = bus.read_i2c_block_data(0x23, 0x20, 2)
        result = (data[1] + (256 * data[0])) / 1.2
    """
    
    def __init__(self, i2c_address: int = 0x23):
        super().__init__(name="light", unit="lux")
        self.i2c_address = i2c_address
        # Initialize hardware here
    
    def read(self) -> float:
        """
        Read from actual hardware sensor.
        This is a placeholder - implement actual hardware reading.
        """
        # TODO: Implement actual sensor reading
        # Example: return self.read_i2c_light_value()
        raise NotImplementedError("Real sensor implementation required")
