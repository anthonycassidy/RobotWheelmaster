"""
Raspberry Pi 5 GPIO Pin Configuration
===================================

This file contains the pin mapping configuration for the robot's hardware components.
All pin numbers use BCM (Broadcom) numbering scheme.

Hardware Connected:
- 4x L298N Motor Drivers (one for each wheel)
- 4x Servo Motors (for steering)
- Camera Module (uses dedicated camera interface)

Pin Layout:
===========

Motor Drivers (L298N):
---------------------
Front Left Motor:
    - Enable: GPIO 17
    - Input 1: GPIO 27
    - Input 2: GPIO 22
    
Front Right Motor:
    - Enable: GPIO 23
    - Input 1: GPIO 24
    - Input 2: GPIO 25
    
Rear Left Motor:
    - Enable: GPIO 5
    - Input 1: GPIO 6
    - Input 2: GPIO 13
    
Rear Right Motor:
    - Enable: GPIO 12
    - Input 1: GPIO 16
    - Input 2: GPIO 20

Servo Motors:
------------
- Front Left Steering: GPIO 18 (PWM capable)
- Front Right Steering: GPIO 19 (PWM capable)
- Rear Left Steering: GPIO 21 (PWM capable)
- Rear Right Steering: GPIO 26 (PWM capable)

Notes:
- All Enable pins must be PWM capable for speed control
- All servo pins must be PWM capable for position control
- BCM numbering is used throughout
"""

# Motor Driver Pin Configuration
MOTOR_PINS = {
    'front_left': {
        'en': 17,    # Enable pin (PWM)
        'in1': 27,   # Input 1
        'in2': 22,   # Input 2
    },
    'front_right': {
        'en': 23,    # Enable pin (PWM)
        'in1': 24,   # Input 1
        'in2': 25,   # Input 2
    },
    'rear_left': {
        'en': 5,     # Enable pin (PWM)
        'in1': 6,    # Input 1
        'in2': 13,   # Input 2
    },
    'rear_right': {
        'en': 12,    # Enable pin (PWM)
        'in1': 16,   # Input 1
        'in2': 20,   # Input 2
    }
}

# Servo Motor Pin Configuration
SERVO_PINS = {
    'front_left': 18,    # PWM pin for front left steering
    'front_right': 19,   # PWM pin for front right steering
    'rear_left': 21,     # PWM pin for rear left steering
    'rear_right': 26,    # PWM pin for rear right steering
}

# PWM Configuration
PWM_FREQUENCY = 50       # 50Hz for servos
MOTOR_PWM_FREQUENCY = 1000  # 1KHz for motor control
