"""
Configuration settings for the Raspberry Pi Sensor Dashboard
"""

# Server settings
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# Sensor update interval (in seconds)
SENSOR_UPDATE_INTERVAL = 2

# Sensor settings
SENSORS_CONFIG = {
    'temperature': {
        'enabled': True,
        'unit': '°C',
        'min_value': -10,
        'max_value': 40
    },
    'light': {
        'enabled': True,
        'unit': 'lux',
        'min_value': 0,
        'max_value': 1000
    },
    'motion': {
        'enabled': True,
        'unit': 'boolean',
    }
}
