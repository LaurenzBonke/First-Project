// Simplified Raspberry Pi Sensor Dashboard JavaScript
// Using polling instead of WebSocket for simplicity

// Data history for display (keep last 5 points)
const maxDataPoints = 5;
let temperatureHistory = [];
let lightHistory = [];

// Counters and state
let dataPointCount = 0;
let startTime = Date.now();
let motionEvents = [];
let isConnected = false;

// Initialize the dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    startPolling();
    startUptime();
    setupEventListeners();
});

// Start polling for sensor data
function startPolling() {
    updateConnectionStatus(true);
    pollSensorData();
    
    // Poll every 2 seconds
    setInterval(pollSensorData, 2000);
}

// Poll sensor data from server
async function pollSensorData() {
    try {
        const response = await fetch('/api/sensors');
        if (response.ok) {
            const data = await response.json();
            updateDashboard(data);
            if (!isConnected) {
                isConnected = true;
                updateConnectionStatus(true);
            }
        } else {
            throw new Error('Failed to fetch data');
        }
    } catch (error) {
        console.error('Error fetching sensor data:', error);
        if (isConnected) {
            isConnected = false;
            updateConnectionStatus(false);
        }
    }
}

// Update connection status indicator
function updateConnectionStatus(connected) {
    const statusDot = document.getElementById('connectionStatus');
    const statusText = document.getElementById('connectionText');
    
    if (connected) {
        statusDot.classList.add('connected');
        statusDot.classList.remove('disconnected');
        statusText.textContent = 'Connected';
    } else {
        statusDot.classList.remove('connected');
        statusDot.classList.add('disconnected');
        statusText.textContent = 'Disconnected';
    }
}

// Update dashboard with new sensor data
function updateDashboard(data) {
    const currentTime = new Date().toLocaleTimeString();
    
    // Update temperature
    if (data.temperature) {
        updateTemperature(data.temperature, currentTime);
    }
    
    // Update light
    if (data.light) {
        updateLight(data.light, currentTime);
    }
    
    // Update motion
    if (data.motion) {
        updateMotion(data.motion, currentTime);
    }
    
    // Update system info
    dataPointCount++;
    document.getElementById('dataPoints').textContent = dataPointCount;
    document.getElementById('sensorCount').textContent = Object.keys(data).length;
}

// Update temperature display
function updateTemperature(tempData, time) {
    const value = tempData.value;
    const unit = tempData.unit || '°C';
    
    document.getElementById('temperatureValue').textContent = value;
    document.getElementById('temperatureUnit').textContent = unit;
    document.getElementById('temperatureTime').textContent = time;
    
    // Update history
    temperatureHistory.push(value);
    if (temperatureHistory.length > maxDataPoints) {
        temperatureHistory.shift();
    }
    updateHistoryDisplay('temperatureHistory', temperatureHistory, unit);
}

// Update light display
function updateLight(lightData, time) {
    const value = lightData.value;
    const unit = lightData.unit || 'lux';
    
    document.getElementById('lightValue').textContent = value;
    document.getElementById('lightUnit').textContent = unit;
    document.getElementById('lightTime').textContent = time;
    
    // Update light bar (0-1000 lux scale)
    const percentage = Math.min((value / 1000) * 100, 100);
    document.getElementById('lightBar').style.width = percentage + '%';
    
    // Update history
    lightHistory.push(value);
    if (lightHistory.length > maxDataPoints) {
        lightHistory.shift();
    }
    updateHistoryDisplay('lightHistory', lightHistory, unit);
}

// Update motion display
function updateMotion(motionData, time) {
    const detected = motionData.value;
    const status = motionData.status || (detected ? 'Motion Detected' : 'No Motion');
    
    const motionCircle = document.querySelector('.motion-circle');
    const motionStatus = document.getElementById('motionStatus');
    
    motionStatus.textContent = status;
    document.getElementById('motionTime').textContent = time;
    
    if (detected) {
        motionCircle.classList.add('active');
        addMotionEvent(time);
    } else {
        motionCircle.classList.remove('active');
    }
}

// Add motion event to history
function addMotionEvent(time) {
    // Avoid duplicates from the same timestamp
    if (motionEvents.length > 0 && motionEvents[0] === time) {
        return;
    }
    
    motionEvents.unshift(time);
    
    // Keep only last 5 events
    if (motionEvents.length > 5) {
        motionEvents.pop();
    }
    
    // Update motion history display
    const historyList = document.getElementById('motionHistory');
    historyList.innerHTML = '';
    
    motionEvents.forEach(eventTime => {
        const li = document.createElement('li');
        li.textContent = `Motion at ${eventTime}`;
        historyList.appendChild(li);
    });
}

// Update history display with recent values
function updateHistoryDisplay(historyId, dataArray, unit) {
    const historyElement = document.getElementById(historyId);
    if (!historyElement) return;
    
    const valuesContainer = historyElement.querySelector('.history-values');
    if (!valuesContainer) return;
    
    // Show values with arrows
    if (dataArray.length > 0) {
        valuesContainer.textContent = dataArray.map(v => `${v}${unit}`).join(' → ');
    }
}

// Setup additional event listeners
function setupEventListeners() {
    // Manual refresh on pressing 'r'
    document.addEventListener('keydown', (e) => {
        if (e.key === 'r' || e.key === 'R') {
            console.log('Manual data refresh...');
            pollSensorData();
        }
    });
}

// Update uptime counter
function startUptime() {
    setInterval(() => {
        const elapsed = Date.now() - startTime;
        const hours = Math.floor(elapsed / 3600000);
        const minutes = Math.floor((elapsed % 3600000) / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        
        const uptimeStr = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
        document.getElementById('uptime').textContent = uptimeStr;
    }, 1000);
}

// Helper function to pad numbers
function pad(num) {
    return num.toString().padStart(2, '0');
}

// Log initialization
console.log('Dashboard initialized. Polling for sensor data every 2 seconds.');
console.log('Press R to manually refresh data.');
