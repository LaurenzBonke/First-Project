# 🔌 Raspberry Pi Sensor Dashboard

A small interactive sensor dashboard that displays real-time data from Raspberry Pi sensors, such as temperature, light, and motion. This project demonstrates modular hardware sensor reading, data processing, and live visualization through a clean web interface.

## 🌟 Features

- **Modular Sensor Architecture**: Easy-to-extend sensor framework with abstract base class
- **Real-Time Updates**: Live data visualization using HTTP polling
- **Multiple Sensor Support**:
  - 🌡️ Temperature sensor (DHT22, DS18B20 compatible)
  - 💡 Light sensor (BH1750, TSL2561 compatible)
  - 👁️ Motion sensor (PIR sensor compatible)
- **Interactive Dashboard**: Clean, responsive web interface with real-time charts
- **Mock Sensors Included**: Test without hardware using simulated sensors
- **Easy Configuration**: Simple config file for sensor settings

## 📋 Requirements

- Python 3.7+
- Raspberry Pi (any model) for hardware sensors, or any computer for demo mode
- Modern web browser

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/LaurenzBonke/First-Project.git
cd First-Project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

```bash
python app.py
```

### 4. Open Your Browser

Navigate to: `http://localhost:5000`

The dashboard will display real-time sensor data with automatic updates every 2 seconds.

## 📁 Project Structure

```
First-Project/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── sensor_manager.py       # Sensor coordination layer
├── sensors/                # Modular sensor modules
│   ├── __init__.py
│   ├── base_sensor.py      # Abstract sensor base class
│   ├── temperature_sensor.py
│   ├── light_sensor.py
│   └── motion_sensor.py
├── templates/
│   └── index.html          # Dashboard HTML template
├── static/
│   ├── style.css           # Dashboard styles
│   └── dashboard_simple.js # Client-side JavaScript
└── requirements.txt        # Python dependencies
```

## 🔧 Configuration

Edit `config.py` to customize:

- Server host and port
- Sensor update interval
- Enable/disable specific sensors
- Sensor value ranges
- **Debug mode** (set `DEBUG = False` for production)

```python
SENSOR_UPDATE_INTERVAL = 2  # Update every 2 seconds

SENSORS_CONFIG = {
    'temperature': {
        'enabled': True,
        'unit': '°C',
        'min_value': -10,
        'max_value': 40
    },
    # ... more sensor configs
}
```

> ⚠️ **Security Note**: The application runs in debug mode by default for development purposes. 
> Before deploying to production, set `DEBUG = False` in `config.py` and use a production WSGI server like Gunicorn or uWSGI.

## 🔌 Hardware Setup

### Using Real Sensors

1. **Temperature Sensor (DHT22 / DS18B20)**
   - Connect to GPIO pin 4
   - Install library: `pip install Adafruit_DHT` (for DHT22)
   - Update `sensors/temperature_sensor.py` to use `RealTemperatureSensor`

2. **Light Sensor (BH1750)**
   - Connect via I2C (SDA to GPIO 2, SCL to GPIO 3)
   - Install library: `pip install smbus`
   - Update `sensors/light_sensor.py` to use `RealLightSensor`

3. **Motion Sensor (PIR HC-SR501)**
   - Connect to GPIO pin 17
   - Install library: `pip install RPi.GPIO`
   - Update `sensors/motion_sensor.py` to use `RealMotionSensor`

### Demo Mode (No Hardware)

The dashboard runs in demo mode by default with simulated sensors. Perfect for:
- Testing the interface
- Development without hardware
- Demonstrations

## 🎨 Dashboard Features

- **Real-time Charts**: Temperature and light intensity history
- **Motion Detection**: Visual indicator and event log
- **System Info**: Connection status, uptime, and data statistics
- **Responsive Design**: Works on desktop and mobile devices
- **Auto-reconnect**: Handles connection issues gracefully

## 🔨 Adding New Sensors

1. Create a new sensor class inheriting from `BaseSensor`:

```python
from sensors.base_sensor import BaseSensor

class MySensor(BaseSensor):
    def __init__(self):
        super().__init__(name="my_sensor", unit="units")
    
    def read(self):
        # Implement sensor reading logic
        return sensor_value
```

2. Add sensor to `app.py`:

```python
my_sensor = MySensor()
sensor_manager.add_sensor(my_sensor)
```

3. Update the dashboard UI in `templates/index.html` to display the new sensor data.

## 🐛 Troubleshooting

**Connection Issues:**
- Ensure no other application is using port 5000
- Check firewall settings
- Try accessing via `http://127.0.0.1:5000`

**Sensor Not Reading:**
- Verify hardware connections
- Check GPIO pin numbers in sensor configuration
- Ensure required libraries are installed
- Review error messages in console

**Browser Not Updating:**
- Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)
- Check browser console for JavaScript errors
- Verify WebSocket connection in Network tab

## 📚 Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Real-time**: HTTP Polling (REST API)
- **Hardware**: Raspberry Pi GPIO (when using real sensors)

## 🎓 Learning Objectives

This project demonstrates:
- Modular software architecture with abstract classes
- Hardware interfacing and sensor reading
- Real-time web communication with HTTP polling
- Data processing and visualization
- Responsive UI design
- Event-driven programming

## 📝 License

This project is licensed under the terms in the LICENSE file.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add support for new sensors
- Improve the UI/UX
- Add new visualization features
- Enhance documentation

## 🔗 Resources

- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

---

**Note**: This dashboard runs in demo mode with simulated sensors by default. To use real hardware sensors, follow the Hardware Setup instructions above. 
