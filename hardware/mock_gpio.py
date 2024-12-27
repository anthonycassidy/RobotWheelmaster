class MockGPIO:
    OUT = 'out'
    IN = 'in'
    HIGH = 1
    LOW = 0
    BCM = 'bcm'
    
    def __init__(self):
        self.pins = {}
        self.pwm_pins = {}
    
    def setmode(self, mode):
        self.mode = mode
    
    def setup(self, pin, mode):
        self.pins[pin] = {'mode': mode, 'value': 0}
    
    def output(self, pin, value):
        if pin in self.pins:
            self.pins[pin]['value'] = value
    
    def PWM(self, pin, freq):
        if pin not in self.pwm_pins:
            self.pwm_pins[pin] = MockPWM(pin, freq)
        return self.pwm_pins[pin]
    
    def cleanup(self):
        self.pins.clear()
        self.pwm_pins.clear()

class MockPWM:
    def __init__(self, pin, freq):
        self.pin = pin
        self.freq = freq
        self.duty_cycle = 0
        self.running = False
    
    def start(self, duty_cycle):
        self.duty_cycle = duty_cycle
        self.running = True
    
    def ChangeDutyCycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
    
    def stop(self):
        self.running = False

# Create a global instance to be used as a mock
GPIO = MockGPIO()
