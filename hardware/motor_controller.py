from .mock_gpio import GPIO
import logging

class MotorController:
    def __init__(self):
        # GPIO Setup
        GPIO.setmode(GPIO.BCM)

        # Motor driver pins
        self.MOTOR_PINS = {
            'front_left': {'en': 17, 'in1': 27, 'in2': 22},
            'front_right': {'en': 23, 'in1': 24, 'in2': 25},
            'rear_left': {'en': 5, 'in1': 6, 'in2': 13},
            'rear_right': {'en': 12, 'in1': 16, 'in2': 20}
        }

        # Servo pins
        self.SERVO_PINS = {
            'front_left': 18,
            'front_right': 19,
            'rear_left': 21,
            'rear_right': 26
        }

        # Initialize pwm_instances before setup
        self.pwm_instances = {}
        self._setup_gpio()
        logging.info("Motor controller initialized with mock GPIO")

    def _setup_gpio(self):
        # Setup motor control pins
        for motor in self.MOTOR_PINS.values():
            GPIO.setup(motor['en'], GPIO.OUT)
            GPIO.setup(motor['in1'], GPIO.OUT)
            GPIO.setup(motor['in2'], GPIO.OUT)
            # Initialize PWM for speed control
            self.pwm_instances[motor['en']] = GPIO.PWM(motor['en'], 1000)
            self.pwm_instances[motor['en']].start(0)

        # Setup servo pins
        for servo_pin in self.SERVO_PINS.values():
            GPIO.setup(servo_pin, GPIO.OUT)
            self.pwm_instances[servo_pin] = GPIO.PWM(servo_pin, 50)
            self.pwm_instances[servo_pin].start(7.5)  # Center position

    def process_movement(self, left_x, left_y, right_x, right_y):
        try:
            logging.debug(f"Received joystick inputs - Left: ({left_x}, {left_y}), Right: ({right_x}, {right_y})")

            # Convert joystick values to motor speeds and steering angles
            speed = self._calculate_speed(left_y)
            steering = self._calculate_steering(right_x)

            logging.debug(f"Calculated values - Speed: {speed}, Steering angle: {steering}")

            # Apply motor speeds
            for motor_name, motor in self.MOTOR_PINS.items():
                self._set_motor_speed(motor, speed)
                logging.debug(f"Motor {motor_name} - Setting speed to {speed}")

            # Apply steering angles
            for servo_name, servo_pin in self.SERVO_PINS.items():
                self._set_steering_angle(servo_pin, steering)
                logging.debug(f"Servo {servo_name} - Setting angle to {steering}")

        except Exception as e:
            logging.error(f"Error processing movement: {str(e)}")
            self.emergency_stop()
            raise

    def _calculate_speed(self, y_value):
        # Convert y-axis value to speed (-100 to 100)
        return int(y_value * 100)

    def _calculate_steering(self, x_value):
        # Convert x-axis value to angle (0 to 180)
        return 90 + (x_value * 45)

    def _set_motor_speed(self, motor, speed):
        if speed > 0:
            GPIO.output(motor['in1'], GPIO.HIGH)
            GPIO.output(motor['in2'], GPIO.LOW)
        else:
            GPIO.output(motor['in1'], GPIO.LOW)
            GPIO.output(motor['in2'], GPIO.HIGH)

        self.pwm_instances[motor['en']].ChangeDutyCycle(abs(speed))

    def _set_steering_angle(self, servo_pin, angle):
        # Convert angle to duty cycle (2.5 to 12.5)
        duty = 2.5 + (angle / 18.0)
        self.pwm_instances[servo_pin].ChangeDutyCycle(duty)

    def emergency_stop(self):
        logging.info("Emergency stop triggered")
        try:
            for motor in self.MOTOR_PINS.values():
                self.pwm_instances[motor['en']].ChangeDutyCycle(0)
                GPIO.output(motor['in1'], GPIO.LOW)
                GPIO.output(motor['in2'], GPIO.LOW)

            # Center all servos
            for servo_pin in self.SERVO_PINS.values():
                self.pwm_instances[servo_pin].ChangeDutyCycle(7.5)
        except Exception as e:
            logging.error(f"Error during emergency stop: {str(e)}")

    def __del__(self):
        for pwm in self.pwm_instances.values():
            try:
                pwm.stop()
            except:
                pass
        GPIO.cleanup()