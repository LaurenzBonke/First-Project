"""
Raspberry Pi Sensor Dashboard - Main Application
A modular sensor dashboard with real-time updates via WebSocket.
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
from sensor_manager import SensorManager
from sensors import TemperatureSensor, LightSensor, MotionSensor
import config

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'raspberry-pi-sensor-dashboard'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize sensor manager
sensor_manager = SensorManager()

# Flag to control sensor reading thread
reading_active = False


def setup_sensors():
    """
    Initialize and configure all sensors.
    This modular approach allows easy addition of new sensors.
    """
    print("Setting up sensors...")
    
    # Add temperature sensor if enabled
    if config.SENSORS_CONFIG['temperature']['enabled']:
        temp_sensor = TemperatureSensor(
            min_temp=config.SENSORS_CONFIG['temperature']['min_value'],
            max_temp=config.SENSORS_CONFIG['temperature']['max_value']
        )
        sensor_manager.add_sensor(temp_sensor)
    
    # Add light sensor if enabled
    if config.SENSORS_CONFIG['light']['enabled']:
        light_sensor = LightSensor(
            min_light=config.SENSORS_CONFIG['light']['min_value'],
            max_light=config.SENSORS_CONFIG['light']['max_value']
        )
        sensor_manager.add_sensor(light_sensor)
    
    # Add motion sensor if enabled
    if config.SENSORS_CONFIG['motion']['enabled']:
        motion_sensor = MotionSensor(detection_probability=0.15)
        sensor_manager.add_sensor(motion_sensor)
    
    print(f"Setup complete: {sensor_manager.get_sensor_count()} sensors active")


def read_sensors_continuously():
    """
    Background thread that continuously reads sensors and emits data via WebSocket.
    Provides live visualization updates.
    """
    global reading_active
    
    while reading_active:
        # Read all sensor data
        sensor_data = sensor_manager.read_all_sensors()
        
        # Emit data to all connected clients
        socketio.emit('sensor_update', sensor_data, namespace='/')
        
        # Wait before next reading
        time.sleep(config.SENSOR_UPDATE_INTERVAL)


@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')


@app.route('/api/sensors')
def get_sensors():
    """API endpoint to get current sensor data."""
    sensor_data = sensor_manager.read_all_sensors()
    return sensor_data


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    # Send initial sensor data
    sensor_data = sensor_manager.read_all_sensors()
    emit('sensor_update', sensor_data)


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')


@socketio.on('request_data')
def handle_data_request():
    """Handle explicit data request from client."""
    sensor_data = sensor_manager.read_all_sensors()
    emit('sensor_update', sensor_data)


def start_background_reading():
    """Start the background sensor reading thread."""
    global reading_active
    reading_active = True
    
    # Start the sensor reading thread
    thread = threading.Thread(target=read_sensors_continuously, daemon=True)
    thread.start()
    print("Background sensor reading started")


if __name__ == '__main__':
    # Setup sensors
    setup_sensors()
    
    # Start background reading
    start_background_reading()
    
    # Run the Flask-SocketIO server
    print(f"Starting dashboard server on {config.HOST}:{config.PORT}")
    socketio.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG)
