// Raspberry Pi Sensor Dashboard JavaScript
// Handles real-time updates via WebSocket and data visualization

// Initialize Socket.IO connection
const socket = io();

// Chart instances
let temperatureChart = null;
let lightChart = null;

// Data history for charts (keep last 20 points)
const maxDataPoints = 20;
let temperatureHistory = [];
let lightHistory = [];
let timeHistory = [];

// Counters and state
let dataPointCount = 0;
let startTime = Date.now();
let motionEvents = [];

// Initialize the dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    startUptime();
});

// Socket.IO Event Handlers
socket.on('connect', () => {
    console.log('Connected to server');
    updateConnectionStatus(true);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    updateConnectionStatus(false);
});

socket.on('sensor_update', (data) => {
    console.log('Received sensor data:', data);
    updateDashboard(data);
});

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

// Update temperature display and chart
function updateTemperature(tempData, time) {
    const value = tempData.value;
    const unit = tempData.unit || '°C';
    
    document.getElementById('temperatureValue').textContent = value;
    document.getElementById('temperatureUnit').textContent = unit;
    document.getElementById('temperatureTime').textContent = time;
    
    // Update history
    updateChartData(temperatureHistory, value, time);
    updateHistoryDisplay('temperatureHistory', temperatureHistory, unit);
}

// Update light display and chart
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
    updateChartData(lightHistory, value, time);
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

// Update chart data arrays
function updateChartData(dataArray, value, time) {
    dataArray.push(value);
    
    // Update time array only once per update cycle
    if (dataArray === temperatureHistory) {
        timeHistory.push(time);
        
        // Keep only last maxDataPoints
        if (timeHistory.length > maxDataPoints) {
            timeHistory.shift();
        }
    }
    
    // Keep only last maxDataPoints
    if (dataArray.length > maxDataPoints) {
        dataArray.shift();
    }
}

// Update a chart with new data - Simple canvas drawing without Chart.js
function updateChart(chart, data, labels) {
    // Simple implementation - we'll draw basic charts using canvas
    // This is a simplified version for demonstration
}

// Update history display with recent values
function updateHistoryDisplay(historyId, dataArray, unit) {
    const historyElement = document.getElementById(historyId);
    if (!historyElement) return;
    
    const valuesContainer = historyElement.querySelector('.history-values');
    if (!valuesContainer) return;
    
    // Show last 5 values
    const recentValues = dataArray.slice(-5);
    valuesContainer.textContent = recentValues.map(v => `${v}${unit}`).join(' → ');
}

// Initialize Chart.js charts - Simplified without Chart.js library
function initializeCharts() {
    // For now, we'll skip the chart initialization
    // The dashboard will still work with numerical displays
    console.log('Charts simplified - showing data without graphical charts');
}

// Setup additional event listeners
function setupEventListeners() {
    // Request data button if needed
    document.addEventListener('keydown', (e) => {
        if (e.key === 'r' || e.key === 'R') {
            console.log('Requesting data refresh...');
            socket.emit('request_data');
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
console.log('Dashboard initialized. Press R to refresh data.');
