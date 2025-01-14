import os
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import logging
from hardware.motor_controller import MotorController
from hardware.camera import Camera

class SocketIOHandler(logging.Handler):
    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio

    def emit(self, record):
        self.socketio.emit('log', {'message': self.format(record)})

# Set up logging with a more visible format
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'robotcontrol2024'
socketio = SocketIO(app)

# Add SocketIO handler to send logs to frontend
socket_handler = SocketIOHandler(socketio)
socket_handler.setLevel(logging.INFO)
socket_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logging.getLogger().addHandler(socket_handler)

# Initialize hardware controllers
motor_controller = MotorController()
camera = Camera()

logging.info("=== Robot Control Server Starting ===")
logging.info("Video feed initialized")
logging.info("Motor controller initialized")
logging.info("Socket.IO ready for joystick inputs")
logging.info("=====================================")

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('move')
def handle_movement(data):
    try:
        logging.info(f"Received movement data: {data}")
        motor_controller.process_movement(
            data['left_x'], data['left_y'],
            data['right_x'], data['right_y']
        )
        emit('status', {'status': 'ok'})
    except Exception as e:
        logging.error(f"Movement error: {str(e)}")
        emit('status', {'status': 'error', 'message': str(e)})

@socketio.on('emergency_stop')
def handle_emergency_stop():
    try:
        logging.info("Emergency stop triggered via socket event")
        motor_controller.emergency_stop()
        emit('status', {'status': 'stopped'})
    except Exception as e:
        logging.error(f"Emergency stop error: {str(e)}")
        emit('status', {'status': 'error', 'message': str(e)})

@socketio.on('connect')
def handle_connect():
    emit('status', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    motor_controller.emergency_stop()