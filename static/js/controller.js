let leftJoystick, rightJoystick;
const socket = io();

// Connection status handling
socket.on('connect', () => {
    updateStatus('Connected', 'success');
    addLogEntry('Connected to robot control server');
});

socket.on('disconnect', () => {
    updateStatus('Disconnected', 'danger');
    addLogEntry('Disconnected from robot control server');
});

socket.on('status', (data) => {
    if (data.status === 'error') {
        updateStatus(data.message, 'danger');
        addLogEntry('Error: ' + data.message);
    }
});

socket.on('log', (data) => {
    addLogEntry(data.message);
});

function updateStatus(message, type) {
    const statusElement = document.getElementById('status');
    statusElement.textContent = message;
    statusElement.className = `alert alert-${type}`;
}

function addLogEntry(message) {
    const logDisplay = document.getElementById('log-display');
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    const timestamp = new Date().toLocaleTimeString();
    entry.textContent = `[${timestamp}] ${message}`;
    logDisplay.appendChild(entry);
    logDisplay.scrollTop = logDisplay.scrollHeight;
}

// Initialize joysticks
document.addEventListener('DOMContentLoaded', () => {
    const leftOptions = {
        zone: document.getElementById('left-joystick'),
        mode: 'static',
        position: { left: '50%', top: '50%' },
        color: 'var(--bs-info)',
        size: 150
    };

    const rightOptions = {
        zone: document.getElementById('right-joystick'),
        mode: 'static',
        position: { left: '50%', top: '50%' },
        color: 'var(--bs-info)',
        size: 150
    };

    leftJoystick = nipplejs.create(leftOptions);
    rightJoystick = nipplejs.create(rightOptions);

    addLogEntry('Joystick controls initialized');

    let leftData = { x: 0, y: 0 };
    let rightData = { x: 0, y: 0 };

    leftJoystick.on('move', (evt, data) => {
        leftData.x = data.vector.x;
        leftData.y = data.vector.y;
        sendControlData(leftData, rightData);
    });

    leftJoystick.on('end', () => {
        leftData = { x: 0, y: 0 };
        sendControlData(leftData, rightData);
        addLogEntry('Movement stopped');
    });

    rightJoystick.on('move', (evt, data) => {
        rightData.x = data.vector.x;
        rightData.y = data.vector.y;
        sendControlData(leftData, rightData);
    });

    rightJoystick.on('end', () => {
        rightData = { x: 0, y: 0 };
        sendControlData(leftData, rightData);
        addLogEntry('Steering centered');
    });

    // Emergency stop button
    document.getElementById('emergency-stop').addEventListener('click', () => {
        socket.emit('emergency_stop');
        leftData = { x: 0, y: 0 };
        rightData = { x: 0, y: 0 };
        addLogEntry('EMERGENCY STOP ACTIVATED');
    });
});

function sendControlData(leftData, rightData) {
    socket.emit('move', {
        left_x: leftData.x,
        left_y: leftData.y,
        right_x: rightData.x,
        right_y: rightData.y
    });
}