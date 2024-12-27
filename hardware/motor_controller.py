from .mock_gpio import GPIO
from .pin_config import MOTOR_PINS, SERVO_PINS, PWM_FREQUENCY, MOTOR_PWM_FREQUENCY
import logging

class MotorController:
    def __init__(self):
        # GPIO Setup
        GPIO.setmode(GPIO.BCM)

        # Initialize pwm_instances before setup
        self.pwm_instances = {}
        self._setup_gpio()
        logging.info("=== Motor Controller Initialized ===")
        logging.info("Motors configured: front_left, front_right, rear_left, rear_right")
        logging.info("Servos configured: front_left, front_right, rear_left, rear_right")
        logging.info("================================")

    def _setup_gpio(self):
        # Setup motor control pins
        for motor in MOTOR_PINS.values():
            GPIO.setup(motor['en'], GPIO.OUT)
            GPIO.setup(motor['in1'], GPIO.OUT)
            GPIO.setup(motor['in2'], GPIO.OUT)
            # Initialize PWM for speed control
            self.pwm_instances[motor['en']] = GPIO.PWM(motor['en'], MOTOR_PWM_FREQUENCY)
            self.pwm_instances[motor['en']].start(0)

        # Setup servo pins
        for servo_pin in SERVO_PINS.values():
            GPIO.setup(servo_pin, GPIO.OUT)
            self.pwm_instances[servo_pin] = GPIO.PWM(servo_pin, PWM_FREQUENCY)
            self.pwm_instances[servo_pin].start(7.5)  # Center position

    def process_movement(self, left_x, left_y, right_x, right_y):
        try:
            logging.info("=== Movement Command Received ===")
            logging.info(f"Drive Controls: Forward/Back: {left_y:.2f}, Turn: {left_x:.2f}")
            logging.info(f"Steering Controls: Left/Right: {right_x:.2f}, Adjust: {right_y:.2f}")

            # Convert joystick values to motor speeds and steering angles
            speed = self._calculate_speed(left_y)
            steering = self._calculate_steering(right_x)

            logging.info(f"Calculated Speed: {speed}% | Steering Angle: {steering}°")

            # Apply motor speeds
            for motor_name, motor in MOTOR_PINS.items():
                self._set_motor_speed(motor, speed)
                logging.info(f"Motor {motor_name}: Speed set to {speed}%")

            # Apply steering angles
            for servo_name, servo_pin in SERVO_PINS.items():
                self._set_steering_angle(servo_pin, steering)
                logging.info(f"Servo {servo_name}: Angle set to {steering}°")

            logging.info("=== Movement Command Completed ===")

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
            for motor in MOTOR_PINS.values():
                self.pwm_instances[motor['en']].ChangeDutyCycle(0)
                GPIO.output(motor['in1'], GPIO.LOW)
                GPIO.output(motor['in2'], GPIO.LOW)

            # Center all servos
            for servo_pin in SERVO_PINS.values():
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