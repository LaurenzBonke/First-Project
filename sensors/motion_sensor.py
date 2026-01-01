"""
Mock motion sensor for demonstration and testing.
In a real Raspberry Pi setup, this would interface with actual hardware like PIR sensors (HC-SR501).
"""

import random
from .base_sensor import BaseSensor


class MotionSensor(BaseSensor):
    """
    Simulated motion sensor (PIR - Passive Infrared).
    Generates random motion detection events.
    """
    
    def __init__(self, detection_probability: float = 0.2):
        """
        Initialize motion sensor.
        
        Args:
            detection_probability: Probability of detecting motion (0.0 to 1.0)
        """
        super().__init__(name="motion", unit="")
        self.detection_probability = detection_probability
        self._motion_detected = False
    
    def read(self) -> bool:
        """
        Read motion sensor state.
        
        Returns:
            True if motion detected, False otherwise
        """
        # Simulate random motion detection
        self._motion_detected = random.random() < self.detection_probability
        return self._motion_detected
    
    def get_data(self):
        """Override to return user-friendly motion status."""
        value = self.read()
        return {
            'name': self.name,
            'value': value,
            'status': 'Motion Detected' if value else 'No Motion',
            'unit': self.unit
        }


class RealMotionSensor(BaseSensor):
    """
    Template for real motion sensor implementation.
    Replace the read() method with actual hardware communication code.
    
    Example for PIR sensor:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        motion = GPIO.input(pin)
    """
    
    def __init__(self, pin: int = 17):
        super().__init__(name="motion", unit="")
        self.pin = pin
        # Initialize GPIO here
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.pin, GPIO.IN)
    
    def read(self) -> bool:
        """
        Read from actual hardware sensor.
        This is a placeholder - implement actual hardware reading.
        """
        # TODO: Implement actual sensor reading
        # Example: return bool(GPIO.input(self.pin))
        raise NotImplementedError("Real sensor implementation required")
